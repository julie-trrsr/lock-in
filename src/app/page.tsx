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
  const [userId, setUserId] = useState("");
  const [openLogin, setOpenLogin] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");


  const handleSignUp = () => {
    setOpenLogin(false);
  }

  const handleSubmit = () => {
    setOpenLogin(false);
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
      <div className="absolute top-0 right-0 rounded-full hover:bg-neutral-300 hover:cursor-pointer mt-4 mr-4">
        <Login isOpen={openLogin} onClose={() => setOpenLogin(false)}>
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
                onChange={(e) => setUsername(e.target.value)}
                required={true}
              />
            </label>
            <label
              htmlFor="password"
              className="text-left block mb-3 text-lg font-medium text-slate-800"
            >
              Password:
              <input
                id="password"
                className="w-full p-1 border border-slate-300 rounded-md resize-none text-base focus:ring-2 focus:ring-inherit focus:border-inherit focus:outline-none"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required={true}
                type="password"
              />
            </label>
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
          <FaUser className="w-12 h-12 p-2 text-black"
                  title="Log in"
                  onClick={() => setOpenLogin(true)}/>
        ): (
          <>
          </>
        )}
      </div>
      {!lockedIn && !animating ? (
        <div className="flex flex-col gap-8 row-start-2 items-center relative">
          <div onClick={handleUnlockClick} className="hover:cursor-pointer">
            <CiUnlock className="w-20 h-20" />
          </div>
          <div className="text-5xl text-center sm:text-left">
            Lock in!
          </div>
        </div>
      ) : animating ? (
        <div className="flex flex-col gap-8 row-start-2 items-center">
          <motion.div
            className=""
            initial={{ position: "relative", x: "50%", y: "50%", scale: 1}}
            animate={{ position: "absolute", top: 0, left: 0, marginLeft: "1rem", marginTop: "1rem", scale: 0.5 }}
            transition={{ duration: 1, ease: "easeOut" }}
          >
            <CiLock className="w-20 h-20" />
          </motion.div>
        </div>
      ) : (
        <>
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

