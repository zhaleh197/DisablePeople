"use client"
import React from 'react'
import HttpCall from "../../../../components/HttpCall";
import WebSocketCall from "../../../../components/WebSocketCall";
import Videoload from "../../../../components/videoload";
import { io } from "socket.io-client";
import { HiOutlinePlay ,HiOutlineStop} from 'react-icons/hi'
import { useEffect, useState } from "react";
const Main = () => {
    const [socketInstance, setSocketInstance] = useState("");
    const [loading, setLoading] = useState(true);
    const [buttonStatus, setButtonStatus] = useState(false);

    const handleClick = () => {
        if (buttonStatus === false) {
            setButtonStatus(true);
        } else {
            setButtonStatus(false);
        }
    };

    useEffect(() => {
        if (buttonStatus === true) {
            const socket = io("localhost:7001/", {
                transports: ["websocket"],
                cors: {
                    origin: "http://localhost:3000/",
                },
            });

            setSocketInstance(socket);

            socket.on("connect", (data) => {
                console.log(data);
            });

            setLoading(false);

            socket.on("disconnect", (data) => {
                console.log(data);
            });

            return function cleanup() {
                socket.disconnect();
            };
        }
    }, [buttonStatus]);

    return (
        <div className="App" >

            {/* <HttpCall /> */}

            {!buttonStatus ? (
                <div className="flex space-x-4">
                    <button onClick={handleClick} className=" flex px-4 py-2 font-semibold bg-rose-500 text-white rounded-md hover:bg-red-700 space-x-2 align-middle">
                        <HiOutlinePlay className='text-2xl mx-2'></HiOutlinePlay>
                        <span> پخش زنده</span></button>
                </div>
            ) : ( 

                <div className="flex space-x-4">
                    <button onClick={handleClick} className=" flex px-4 py-2 font-semibold bg-orange-500 text-white rounded-md hover:bg-orange-700 space-x-2 align-middle">
                        <HiOutlineStop className='text-2xl mx-2'></HiOutlineStop>
                        <span> توقف پخش</span></button>
                </div>
            )}
            
            <div className='text-center justify-center items-center'>
                {!buttonStatus ? (
                    <>
                    <div className='h-[480px] bg-black w-[640px] mx-auto relative'>

                    </div>
{/* 
<div  dir="rtl" className=' '>
                    <table className='table-auto'>
                    <thead >
                        <tr className='justify-around'>
                        <td className=''><div className=' w-auto' ><div className='h-[480px] bg-black w-[750px] m-16 relative'>

</div></div> </td><div width="900" height="500" className='w-80'></div>             
                        <td  className="object-left " ><div  >
                        <center><img className='object-fill ' src="\green.jpg"  width={300}/>
                        {/* {item.lightflag ==true && <td><center><img className='object-fill ' src="\green.jpg"  width={300}/></center></td>}
                        {item.lightflag ==false &&  <td><center><img className='object-fill ' src="\green.jpg"  width={300}/></center></td>}
                         */}
                        
                        
                        
                        {/* </center>
            
            </div></td></tr></thead ></table></div> */} 
                    </>
                ) : (

                    <>


                    <div className='text-center justify-center items-center'>
                            {!loading && <Videoload socket={socketInstance} />}
                        </div>



                        {/* <div  dir="rtl" className=' '>
                    <table className='table-auto'>
                    <thead >
                        <tr className='justify-around'>
                        <td className=''><div className=' w-auto' ><div className='h-[480px] bg-black w-[750px] m-16 relative'>

</div></div> </td><div width="900" height="500" className='w-80'></div>             
                        <td  className="object-left " ><div  >
                        <center><img className='object-fill ' src="\green.jpg"  width={300}/>
                        {/* {item.lightflag ==true && <td><center><img className='object-fill ' src="\green.jpg"  width={300}/></center></td>}
                        {item.lightflag ==false &&  <td><center><img className='object-fill ' src="\green.jpg"  width={300}/></center></td>} */}
                        
                        
                        
                        
                        {/* </center>
            
            </div></td></tr></thead ></table></div> */}
                    </>
                )}

            </div>
           
        </div>
    );
}
export default Main