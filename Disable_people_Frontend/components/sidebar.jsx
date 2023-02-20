"use client"
import React from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { BiCctv } from 'react-icons/bi'

import { HiOutlineEye, HiOutlineUserGroup, HiOutlinePresentationChartLine } from 'react-icons/hi'
import Videoloadhh from './report'
import Report from './report'
const Sidebar = ({ toggle }) => {
    return (
        <div className='bg-gray-300-600 w-[200px] h-screen  text-gray-700 py-4 border-l-2 border-gray-200'>

            <div className='justify-center my-2 items-center justify-items-center w-full text-center'>
                {/* <div className="h-[120px] w-[120px] bg-red-100 border-2 border-red-500 rounded-full relative mx-auto"></div> */}
                {/* <div className="h-[120px] w-[120px] bg-red-100 border-2 mx-auto rounded-full"><img src= "/logo.png" class='object-cover rounded-full' alt="main" width={200} height={5}/></div> */}
                <h3>
                   Westco
                </h3>
            </div>
            <ul className='px-4 space-y-2  font-semibold'>
                <li>
                    <Link href="/admin/main" className='flex space-x-2 hover:text-pink-700'>
                        <HiOutlineEye className='mx-2'></HiOutlineEye>
                        <span>پخش زنده</span></Link>
                </li>
                <li>
                    <Link href="/report" className='flex space-x-2  hover:text-pink-700'>
                        <HiOutlinePresentationChartLine className='mx-2'></HiOutlinePresentationChartLine>
                        <span>گزارشات  </span></Link>
                </li>
                <li>
                    <Link href="/admin/main" className='flex space-x-2  hover:text-pink-700'>
                        <BiCctv className='mx-2'></BiCctv>
                        <span>  دوربین  ها</span></Link>
                </li>
                {/* <li>
                    <Link href="/admin/main" className='flex space-x-2  hover:text-pink-700'>
                        <HiOutlineUserGroup className='mx-2'></HiOutlineUserGroup>
                        <span>مدیریت کاربران</span></Link>
                </li> */}
            </ul>
        </div>
    )
}

export default Sidebar