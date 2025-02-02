"use client"

import { useSearchParams } from "next/navigation";
import React, { useEffect, useState } from "react";

// (message_id, log_id, time, content)
type Message = [string, string, string, string];

export default function Home() {

    const [messages, setMessages] = useState<Message[]>([
        ["1","2","01/02/2025 04:00","This is the content of the first message."], 
        ["2","2","02/02/2025 11:40","This is the content of the second message."]
    ]);
    const searchParams = useSearchParams();
    const userId = searchParams.get("userId") || ""; // Get userId from URL query

    // useEffect(() => {
    //     async function getMessages() {
    //         if (!userId) return;

    //         const messages = await fetch(`http://172.20.10.11:5000/getPastMessages`, {
    //             method: 'POST', 
    //             headers: {"Accept": "application/json" },
    //             body: JSON.stringify({ userID: userId })
    //           }) 
    //               .then(response => response.json())
    //               .then(data => { return data.messages; });
          
    //           if (messages != null) {
    //             console.log(`messages: ${messages}`);
    //             setMessages(messages);
    //           }
    //     }
    //     getMessages();

    // }, []); //TODO: put userId?

    return (
        <div className="flex flex-col items-center justify-center min-h-screen p-8 sm:p-20">
          <div className="w-full max-w-4xl bg-white shadow-lg rounded-2xl p-6">
            <h1 className="text-3xl font-bold text-center text-black-800 mb-6">
              Message History
            </h1>
            {messages.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full border-collapse border border-gray-300 shadow-md rounded-lg">
                  <thead>
                    <tr className="bg-gray-100 text-black-700">
                      <th className="border border-gray-300 px-6 py-3 text-left">Message ID</th>
                      <th className="border border-gray-300 px-6 py-3 text-left">Log ID</th>
                      <th className="border border-gray-300 px-6 py-3 text-left">Time</th>
                      <th className="border border-gray-300 px-6 py-3 text-left">Content</th>
                    </tr>
                  </thead>
                    <tbody>
                        {[...messages]
                        .sort((a, b) => {
                            // Parse the time strings into Date objects for correct sorting
                            const dateA = new Date(a[2].replace(/(\d{2})\/(\d{2})\/(\d{4}) (\d{2}):(\d{2})/, '$2/$1/$3 $4:$5'));
                            const dateB = new Date(b[2].replace(/(\d{2})\/(\d{2})\/(\d{4}) (\d{2}):(\d{2})/, '$2/$1/$3 $4:$5'));
                            return dateB.getTime() - dateA.getTime();
                        })
                        .map(([message_id, log_id, time, content]) => (
                        <tr key={message_id} className="hover:bg-gray-100 even:bg-gray-50">
                            <td className="border border-gray-300 px-6 py-3 text-black-700">{message_id}</td>
                            <td className="border border-gray-300 px-6 py-3 text-black-700">{log_id}</td>
                            <td className="border border-gray-300 px-6 py-3 text-black-700">{time}</td>
                            <td className="border border-gray-300 px-6 py-3 text-black-700 break-words max-w-xs">
                            {content}
                            </td>
                        </tr>
                        ))}
                    </tbody>
                </table>
              </div>
            ) : (
              <p className="text-center text-black-500 text-lg mt-4">
                No messages found.
              </p>
            )}
          </div>
        </div>
      );      
}