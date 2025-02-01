"use client"
import { useState } from "react";
import { FaUser } from "react-icons/fa"
import { CiUnlock, CiLock } from "react-icons/ci";
import { GoogleOAuthProvider } from '@react-oauth/google';

export default function Home() {
  const [lockedIn, setLockedIn] = useState(false);

  return (
    <div className="relative flex flex-col items-center justify-center justify-items-center min-h-screen p-8 sm:p-20">
      <div className="absolute top-0 right-0 rounded-full hover:bg-neutral-300 hover:cursor-pointer mt-4 mr-4">
        <FaUser className="w-12 h-12 p-2 text-black"/>
      </div>
      {!lockedIn ? (
        <div className="flex flex-col gap-8 row-start-2 items-center">
          <div onClick={e => setLockedIn(true)} className="hover:cursor-pointer">
            <CiUnlock className="w-20 h-20" />
          </div>
          <div className="text-5xl text-center sm:text-left">
            Lock in!
          </div>
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


function Message({
  timecode,
  content
}: {
  timecode: string,
  content: string
}) {
  return (
    <div className="flex flex-row">
      <p className="mr-4 text-stone-500">
        {timecode}
      </p>
      <p className="">
        {content}
      </p>
    </div>
  );
}

