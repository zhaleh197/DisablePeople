"use client";

import Cookies from "js-cookie";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import toast, { Toaster } from "react-hot-toast";


const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("kami2023");
  const router = useRouter();


//  let x =Cookies.get('token',data.token)
  const Log = async (e) => {
    e.preventDefault();
    if (username === "" || password == "") {
        toast.error("تمامی  فیلد الزامی است!");
        return;
      }
    try {
      const res = await fetch("http://127.0.0.1:8000/signin/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        //   Authorization: "Token 536d28a3ec24f650ade5359543c8817ff406da56",
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });
      const data = await res.json();
      if(res.status===200){
        toast.success('با موفقیت وارد شدید')
        router.push('/admin/main')
      }
      if(res.status===404){
        toast.error(' کاربر وجود ندارد')
      }
      console.log(data);
      Cookies.set("token", data.token, {expires: 7});
    //   let x =Cookies.get('token',data.token)
    //   Cookies.set("name", username);
    } catch (err) {
      console.log("ERR", err);
    }
  };

  return (
    <>
      <Toaster />
        <div dir="rtl" className="h-screen font-sans login bg-cover text-black">
          <div className="container mx-auto h-full flex flex-1 justify-center items-center">
            <div className="w-full max-w-lg">
              <div className="leading-loose">
                <div
                  className="max-w-sm m-4 p-10 bg-white bg-opacity-25 rounded shadow-xl"
                >
                  <p className=" font-medium text-center text-lg ">ورود</p>
                  <div className="">
                    <label className="block text-sm " htmlFor="email">
                      نام کاربری
                    </label>
                    <input
                      onChange={(e) => setUsername(e.target.value)}
                      className="w-full px-5 py-1 text-gray-700 bg-gray-300 rounded focus:outline-none focus:bg-white"
                      type="text"
                      id="email"
                      placeholder="UserName"
                      aria-label="email"
                    />
                  </div>
                  <div className="mt-2">
                    <label className="block  text-sm ">رمز</label>
                    <input
                      onChange={(e) => setPassword(e.target.value)}
                      className="w-full px-5 py-1 text-gray-700 bg-gray-300 rounded focus:outline-none focus:bg-white"
                      type="password"
                      id="password"
                      placeholder="Password"
                      arial-label="password"
                    />
                  </div>

                  <div className="mt-4 items-center flex justify-between">
                    <button
                      onClick={Log}
                      className="px-4 py-1  font-light tracking-wider bg-purple-400 hover:bg-pink-400-800 rounded"
                      type="submit"
                    >
                      ورود
                    </button>
                    {/* <a
                      className="inline-block right-0 align-baseline font-bold text-sm text-500  hover:text-red-400"
                      href="#"
                    >
                      Esqueceu a senha ?
                    </a> */}
                  </div>
                  {/* <div className="text-center">
                    <a className="inline-block right-0 align-baseline font-light text-sm text-500 hover:text-red-400">
                      Criar uma conta
                    </a>
                  </div> */}
                </div>
              </div>
            </div>
          </div>
        </div>
  
    </>
  );
};

export default Login;
