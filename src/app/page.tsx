"use client"
import Image from "next/image";
import { useState } from "react";
import { FaUser } from "react-icons/fa"
import { CiUser, CiUnlock, CiLock } from "react-icons/ci";

export default function Home() {
  const [lockedIn, setLockedIn] = useState(false);

  return (
    <div className="flex flex-1 items-center justify-center justify-items-center min-h-screen p-8 sm:p-20">
      <div className="absolute top-0 right-0 rounded-full hover:bg-neutral-300 hover:cursor-pointer mt-4 mr-4">
        <FaUser className="w-12 h-12 p-2 text-black"/>
      </div>
      <div className="flex flex-col gap-8 row-start-2 items-center">
        <CiUnlock className="w-20 h-20 hover:cursor-pointer" />
        <div className="text-5xl text-center sm:text-left">
          Lock in!
        </div>
      </div>
    </div>
  );
}
