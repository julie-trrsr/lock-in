"use client"
import { useState } from "react";
import { FaUser } from "react-icons/fa"
import { CiUnlock, CiLock } from "react-icons/ci";
import { motion } from "framer-motion";
import React from "react";
import { Login } from "@/components/Login";
import { Message } from "@/components/Message";


export default function Home() {
  const [lockedIn, setLockedIn] = useState(false);
  const [animating, setAnimating] = useState(false);
  const [userId, setUserId] = useState("a");
  const [openLogin, setOpenLogin] = useState(false);
  const [openUserModal, setOpenUserModal] = useState(false);
  const [username, setUsername] = useState("maria");
  const [password, setPassword] = useState("");
  const [incorrectPassword, setIncorrectPassword] = useState(false);
  const [userAlreadyExists, setUserAlreadyExists] = useState(false);


  const handleSignUp = async () => {
    const userID = await fetch('http://172.20.10.11:5000/addNewUser', {
      method: 'POST', 
      headers: {"Accept": "application/json" },
      body: JSON.stringify({ username:username, password:password })
    }) 
        .then(response => response.json())
        .then(data => { return data.userID; });
    if (userID == null) {
      setUserAlreadyExists(true);
      setUsername("");
    } else {
      setUserId(userID);
      setPassword("");
      setOpenLogin(false);
    }
  }

  const handleSubmit = async () => {
    const userID = await fetch(`http://172.20.10.11:5000/tryLogin`, {
      method: 'POST', 
      headers: {"Accept": "application/json" },
      body: JSON.stringify({ username:username, password:password })
    }) 
        .then(response => response.json())
        .then(data => { return data.userID; });
    if (userID == null) {
      setPassword("");
      setIncorrectPassword(true);
    } else {
      setUserId(userID as string);
      setPassword("");
      setOpenLogin(false);
    }
  }

  const handleUnlockClick = () => {
    setAnimating(true);
    setTimeout(() => {
      setLockedIn(true);
      setAnimating(false);
    }, 1000);
  };

  return (
    <div className="relative flex flex-col items-center justify-center justify-items-center min-h-screen p-8 sm:p-20">
      {!lockedIn && !animating ? (
        <>
          <div className="absolute top-0 right-0 rounded-full mt-4 mr-4">
            <Login isOpen={openLogin} onClose={() => { setUsername(""); setPassword(""); setIncorrectPassword(false); setUserAlreadyExists(false); setOpenLogin(false); } }>
              <div className="flex flex-col">
                <label
                  htmlFor="username"
                  className="text-left block mb-3 text-lg font-medium text-slate-800"
                >
                  Username:
                  <input
                    id="username"
                    className="w-full p-1 border border-slate-300 rounded-md resize-none text-base focus:ring-2 focus:ring-inherit focus:border-inherit focus:outline-none"
                    value={username}
                    onChange={(e) => { setIncorrectPassword(false); setUserAlreadyExists(false); setUsername(e.target.value); }}
                    required={true}
                  />
                </label>
                {userAlreadyExists && (
                  <p className="text-md text-red-600 text-left">
                    Username already taken, please try again.
                  </p>
                )}
                <label
                  htmlFor="password"
                  className="text-left block mb-3 mt-3 text-lg font-medium text-slate-800"
                >
                  Password:
                  <input
                    id="password"
                    className="w-full p-1 border border-slate-300 rounded-md resize-none text-base focus:ring-2 focus:ring-inherit focus:border-inherit focus:outline-none"
                    value={password}
                    onChange={(e) => { setIncorrectPassword(false); setUserAlreadyExists(false); setPassword(e.target.value); }}
                    required={true}
                    type="password"
                  />
                </label>
                {incorrectPassword && (
                  <p className="text-md text-red-600 text-left">
                    Incorrect username or password, please try again.
                  </p>
                )}
                <div className="flex w-full justify-center items-center mb-2 mt-3">
                  <div className="w-full text-white text-center text-lg font-medium p-1 px-4 bg-blue-400 hover:bg-blue-500 rounded-xl hover:cursor-pointer" onClick={handleSubmit}>
                    Enter
                  </div>
                </div>
                <div className="flex w-full justify-center items-center">
                  <div className="text-center hover:underline hover:cursor-pointer text-lg font-medium p-1 rounded-xl" onClick={handleSignUp}>
                    Sign up
                  </div>
                </div>
              </div>
            </Login>
            {userId == "" ? (
              <FaUser className="hover:bg-neutral-300 rounded-full w-12 h-12 p-2 text-black hover:cursor-pointer"
                      title="Log in"
                      onClick={() => setOpenLogin(true)}/>
            ) : (
              <div  className="flex flex-col items-end"
                    onMouseEnter={() => setOpenUserModal(true)} 
                    onMouseLeave={() => setOpenUserModal(false)}>
                <div className="flex w-12 h-12 bg-black rounded-full justify-center items-center hover:cursor-default">
                  <p className="text-xl text-white text-center p-2">
                    {username.charAt(0).toUpperCase()}
                  </p>
                </div>
                {openUserModal && (
                  <div className="mt-2 w-28  rounded-xl shadow-lg z-50">
                    <ul className="text-end">
                      <li className="px-4 py-2 mb-0.5 text-sm cursor-default text-gray-500">{username}</li>
                      <li className="px-4 py-2 hover:bg-gray-200 cursor-pointer">History</li>
                      <li className="px-4 py-2 hover:bg-gray-200 cursor-pointer" onClick={() => { 
                        setUserId("");
                        setUsername("");
                        setPassword("");
                        setUserAlreadyExists(false);
                        setIncorrectPassword(false); 
                        }}>Log out</li>
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
          <div className="flex flex-col gap-8 row-start-2 items-center relative">
            <div onClick={handleUnlockClick} className="hover:cursor-pointer">
              <CiUnlock className="w-20 h-20" />
            </div>
            <div className="text-5xl text-center sm:text-left">
              Lock in!
            </div>
          </div>
        </>
      ) : animating ? (
        <>
          {userId != "" && (
            <div className="absolute top-0 right-0 rounded-full hover:bg-neutral-300 mt-4 mr-4">
              <div className="flex w-12 h-12 bg-black rounded-full justify-center items-center hover:cursor-default">
                <p className="text-xl text-white text-center p-2">
                  {username.charAt(0).toUpperCase()}
                </p>
              </div>
            </div>
          )}
          <div className="flex flex-col gap-8 row-start-2 items-center">
            <motion.div
              className=""
              initial={{ position: "absolute", top: "44%", left: "50%", transform: "translate(-50%, -50%) scale(1)"}}
              animate={{ position: "fixed", top: 0, left: 0, marginLeft: "2.75rem", marginTop: "2.75rem", transform: "translate(-50%, -50%) scale(0.5)" }}
              transition={{ duration: 1, ease: "easeOut" }}
            >
              <CiLock className="w-20 h-20" />
            </motion.div>
          </div>
        </>
      ) : (
        <>
          {userId != "" && (
            <div className="absolute top-0 right-0 rounded-full hover:bg-neutral-300 mt-4 mr-4">
              <div className="flex w-12 h-12 bg-gray-400 rounded-full justify-center items-center hover:cursor-default">
                <p className="text-xl text-white text-center p-2">
                  {username.charAt(0).toUpperCase()}
                </p>
              </div>
            </div>
          )}
          <div className="absolute top-0 left-0 ml-4 mt-4 hover:cursor-pointer" onClick={e => setLockedIn(false)}>
            <CiLock className="w-14 h-14 p-2" />
          </div>
          <div className="flex flex-1 w-full">
            <div className="basis-2/3 p-4 pr-2">
              <div className="bg-stone-800 w-full h-full rounded-2xl"></div>
            </div>
            <div className="basis-1/3 p-4 pl-2">
              <div className="flex flex-col bg-stone-200 w-full h-full rounded-2xl items-start justify-start">
                <div className="rounded-2xl w-full h-full text-black text-base text-left p-4">
                  <Message timecode="10:30" content="This is the first message" />
                  <Message timecode="11:30" content="This is the second message" />
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

