"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";

export default function Login() {
  const router = useRouter();

  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (token !== null) {
      router.push("/", { scroll: false });
    }
  }, []);

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    setLoading(true);

    if (login === "" || password === "") {
      alert("Заполните обязательные поля");
    } else {
      fetch("http://localhost:8001/auth/token", {
        method: "POST",
        body: JSON.stringify({
          username: login,
          password: password,
          client_id: "zipinfo",
        }),
        headers: {
          "Content-Type": "application/json;charset=utf-8",
        },
      })
        .then((response) => response.json())
        .then((json) => {
          localStorage.setItem("accessToken", json.access_token);
          router.push("/", { scroll: false });
        })
        .catch((error) => console.log(error));
    }

    setLoading(false);
  };

  return (
    <div className="h-full flex items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="bg-neutral-200 rounded-xl px-6 py-4 flex flex-col gap-4"
      >
        <label>Логин</label>
        <input
          onChange={(e) => setLogin(e.target.value)}
          className="h-8 px-3 py-1 border border-neutral-400 rounded-lg"
        />
        <label>Пароль</label>
        <input
          type="password"
          onChange={(e) => setPassword(e.target.value)}
          className="h-8 px-3 py-1 border border-neutral-400 rounded-lg"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-500 w-max px-4 py-2 rounded-lg hover:bg-blue-400 disabled:bg-neutral-400"
        >
          Войти
        </button>
      </form>
    </div>
  );
}
