"use client"
import Sidebar from '../../../components/sidebar';
import Header from '../../../components/header';
import React, { useState } from 'react';
import '../../globals.css'
import Report from '../../../components/report';
function RootLayout({ children }) {

    return (

        <html lang="en">
            <head>
                <meta charset="UTF-8" />
                <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>سامانه پاریز</title>
            </head>
            <body>
                <div className="flex bg-green-100">
                    <Sidebar></Sidebar>
                    
                    <main className='w-full'>
                        <Header></Header>
                        <article className='m-4 border-2 p-4'>
                            {children}
                        </article>
                    </main>
                </div>
            </body>
        </html>
    );
}

export default RootLayout;