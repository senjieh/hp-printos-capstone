"use client";
import Image from "next/image";
import { useState } from "react";

export default function Home() {
  const [data, setData] = useState<{_id: string, print_data: string}[]>([]);

  async function fetchData() {
    try {
      const response = await fetch('http://localhost:4001/data');
      const fetch_data = await response.json();

      console.log(fetch_data['response']);  // Log the data
      setData(fetch_data['response']);      // Set the data to state here
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }
  
  const handleClick = () => {
    fetchData();  // Just call fetchData, no need to set state here
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1>Print Data</h1>
      {data.map((item, index) => (
          <p key={index}>{item.print_data}</p>
      ))}

      <button onClick={handleClick}>Click me for data</button>
    </main>
  );
}
