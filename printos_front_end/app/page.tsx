"use client";
import Image from "next/image";
import { useState } from "react";

export default function Home() {
  const [data, setData] = useState<{ _id: string; text: string }[]>([]);

  async function fetchData() {
    try {
      const response = await fetch("https://cat-fact.herokuapp.com/facts"); // Fetching data
      const fetch_data = await response.json(); // Ensuring data is json

      console.log(fetch_data); // Printing to console
      setData(fetch_data); // Set the data to fetch_data
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }

  const handleClick = () => {
    fetchData(); // Just call fetchData, no need to set state here
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1>Mapped Array Data</h1>
      {/* Map fetched data */}
      {data.map((item, index) => (
        <p key={index}>{item.text}</p>
      ))}

      <button onClick={handleClick}>Click me to fetch data</button>
    </main>
  );
}
