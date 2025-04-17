"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useEffect, useRef, useState } from "react";

export default function Home() {
  const router = useRouter();

  const [loading, setLoading] = useState(false);
  const [task, setTask] = useState("");

  const [result, setResult] = useState("");

  const fileInput = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (token !== null) {
      router.push("/login", { scroll: false });
    }
  }, []);

  useEffect(() => {
    if (task !== "") {
      const intervalId = setInterval(() => {
        fetch(`http://localhost:8000/report/${task}`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
          .then((response) => response.json())
          .then((json) => {
            setResult(JSON.stringify(json));

            if (json?.status === "SUCCESS") {
              clearInterval(intervalId);
            }
          })
          .catch((error) => console.log(error));
      }, 5000);

      return () => clearInterval(intervalId);
    }
  }, [task]);

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();

    setLoading(true);

    if (fileInput.current && fileInput.current.files) {
      if (fileInput.current.files.length > 0) {
        const data = new FormData();
        data.append("file", fileInput.current.files[0]);

        fetch("http://localhost:8000/upload", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
          body: data,
        })
          .then((response) => response.json())
          .then((json) => setTask(json.task_id))
          .catch((error) => console.log(error));
      }
    }
  };

  return (
    <div className="h-full flex items-center justify-center">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
          Upload file
        </label>
        <input
          ref={fileInput}
          type="file"
          className="text-sm text-stone-500
   file:mr-5 file:py-1 file:px-3 file:border-[1px]
   file:text-xs file:font-medium
   file:bg-stone-50 file:text-stone-700
   hover:file:cursor-pointer hover:file:bg-blue-50
   hover:file:text-blue-700"
        />
        <button
          type="submit"
          disabled={loading}
          className="w-max rounded-xl px-4 py-2 bg-blue-500 hover:bg-blue-400 disabled:bg-neutral-400 text-white"
        >
          Отправить на проверку
        </button>
        {loading && <p>Загрузка...</p>}
        {result && (
          <div className="h-full bg-gray-900 text-green-200 font-mono text-sm p-4 rounded-lg w-[600px] shadow-md">
            <pre className="text-wrap">
              <code id="jsonOutput">{result}</code>
            </pre>
          </div>
        )}
      </form>
    </div>
  );
}
