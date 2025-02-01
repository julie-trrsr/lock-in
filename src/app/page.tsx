"use client"
import Image from "next/image";
import { useState } from "react";

export default function Home() {
  const [lockedIn, setLockedIn] = useState(false);

  return (
    <div className="flex flex-1 items-center justify-center justify-items-center min-h-screen p-8 sm:p-20">
      <div className="flex flex-col gap-8 row-start-2 items-center">
        <Image
          className="dark:invert"
          src="/next.svg"
          alt="Next.js logo"
          width={180}
          height={38}
          priority
        />
        <div className="text-5xl text-center sm:text-left">
          Lock in!
        </div>
      </div>
    </div>
  );
}
