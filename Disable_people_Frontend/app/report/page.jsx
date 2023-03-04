 "use client"
// import React, { useState, useEffect } from 'react'
// var L="Red"
// const Videoloadhh = ({ socket }) => {

//     const [frame, setframe] = useState("")
//     const [results, setresults] = useState([])
//     useEffect(() => {
//         const interval = setInterval(() => {
//             socket.emit('request-frame', {});
//         }, 1);

//         socket.on("new-frame", (data) => {
//             setframe(data.base64)
//             // console.log(typeof(data.rec))
//             if (data.rec != null) {
//                 // setframe(data.rec["main_image"])
//                 if (results.length > 5) {
                    
//                     setresults(results.slice(results.length-5, results.length-1))
//                 }
//                 else{
//                 setresults([...results, data.rec])}
                
//             }

//         })

//         return () => {
//             socket.off("new-frame", () => {
//                 console.log("first")
//             })
//         }
//     }, [socket, results, frame])

//     return (
//         <div>
//             <div className='h-[320px] bg-black w-[640px] mx-auto relative py-2'>
//                 <img src={`data:image/jpeg;base64,${frame}`} alt="" className='w-full h-[320px]' />
//             </div>


//             <div className="flex flex-col border-2 h-[300px] overflow-x-hidden mt-4">
//                 <div className="overflow-x-auto sm:-mx-6 lg:-mx-8">
//                     <div className="py-2 inline-block min-w-full sm:px-6 lg:px-8">
//                         <div className="overflow-hidden">
//                             <table className="min-w-full table-auto tbl">
//                                 <thead >
//                                     <tr>
//                                         <th>ردیف</th>
//                                         <th>تاریخ</th>
//                                         <th>چراغ</th>
//                                         <th>نوع معلولیت </th>
//                                         <th>تصویر گرفته شده</th>
//                                         </tr>
//                                 </thead>
//                                 <tbody>

//                                     {

//                                         results.length > 1 ? (
//                                             results.map((item, index) => {
//                                                 return <tr key={index} className="border-2 border-gray-200">
//                                                     <td>{index}</td>
//                                                      <td>{item.date_created}</td>
                                                     
//                                                      {/* <script>
//                                                         var el = document.getElementById('content');
//                                                         var content;
//                                                         if  ({item.lightflag}==true) {
//                                                             content = '<td> Green0</td> '
//                                                         }
//                                                         if  ({item.lightflag}==false) {
//                                                             content = '<td> Red11</td> '
//                                                         }
//                                                         el.insertAdjacentHTML('afterbegin', content);

//                                                      </script> */}


//                                                      <td> {item.lightflag}</td> 
//                                                      <td>{item.classobj}</td>

//                                                     {/* <td>{`data:image/png;base64,${item.img}`}</td> */}
//                                                     <td><img src={`data:image/png;base64,${item.img}`}  width={100}/></td>
//                                                     {/* <td><img src={"http://127.0.0.1:8000/detect" + item.img}/></td> */}
//                                                     {/* {console.log('image',`${item.img}`)} */}
                                                     
                                                    
//                                                 </tr>
//                                             })) : <></>}

//                                 </tbody>
//                             </table>
//                         </div>
//                     </div>
//                 </div>
//             </div>
//         </div>)
// }

// export default Videoloadhh



import Sidebar from '../../components/sidebar';
import Header from '../../components/header';
import React, { useEffect, useState } from 'react';
import persian from 'react-date-object/calendars/persian';
import persian_fa from 'react-date-object/locales/persian_fa';
import DatePicker from 'react-multi-date-picker';
import { Controller, useForm } from 'react-hook-form';
import {
  digitsArToFa,
  digitsArToEn,
  digitsEnToFa,
  digitsFaToEn,
  digitsEnToAr,
  digitsFaToAr,
} 



from '@persian-tools/persian-tools';
import gregorian from 'react-date-object/calendars/gregorian';
import gregorian_en from 'react-date-object/locales/gregorian_en';
import Cookies from 'js-cookie';


const Report = () => { 

    const { control, handleSubmit } = useForm();
    const [submitFirst, setSubmitFirst] = useState();
    const [submitSecond, setSubmitSecond] = useState();
    const [results, setResult] = useState([]);
    

  let x = submitFirst?.format?.('YYYY-MM-DD');
  let y = submitSecond?.format?.('YYYY-MM-DD');
  // var en_number = "0123456789";
// let token
  console.log(x);
  console.log(y);

  const getCity = async (e) => {
    let token  = Cookies.get('token')

    // e.preventDefault()
    try {
      const resApi = await fetch('http://127.0.0.1:8000/date_filter/', {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify({
            startdate: x,
            enddate: y,
        }),
      });

      const data = await resApi.json();
      setResult(data);
      console.log(data);
      console.log('status', resApi.status);
    } catch (e) {
      console.log(e.message);
    }
  };

     


     

      return (


      
      // <div>
     
      <div className='bg-green-100 '>
  <Header></Header>
           
                    
                
        



                   
      <div className='  bg-green-100 h-[120px]  w-[640px] mx-auto relative py-2'>
        {/* <label for="default-input" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">از تاریخ</label>

        <input type="text" id="first_name" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500   block w-100 h-8 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder=" " />
        <label for="default-input" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"> تا تاریخ</label>
        <input type="text" id="first_name" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500   block w-100 h-8 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder=" " /> */}
        
        <div>
        
          <div className="flex justify-center items-center mt-5  gap-x-10">
            <div>
              <label>از تاریخ </label>
              <DatePicker
                inputclassName="form-control"
                required
                calendar={persian}
                locale={persian_fa}
                value={submitFirst}
                onChange={setSubmitFirst}
                format="YYYY-MM-DD"
              />
            </div>
            
            <div>
              <label>تا تاریخ </label>
              <DatePicker
                inputclassName="form-control"
                required
                calendar={persian}
                locale={persian_fa}
                value={submitSecond}
                onChange={setSubmitSecond}
                format="YYYY-MM-DD"
              />
            </div>
          </div>
        </div>
       
      </div> 


      
      <div dir="ltr" className='ml-20'>
     
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4  rounded" 
        onClick={() => getCity()}>
          گزارش
        
        </button></div>


      <div className="flex flex-col border-2 h-[300px] overflow-x-hidden mt-4">
        
          <div className="overflow-x-auto sm:-mx-6 lg:-mx-8">
              <div className="py-2 inline-block min-w-full sm:px-6 lg:px-8">
                  <div className="overflow-hidden">
                    
                      <table className="w-full border-collapse font-bold content-center border-red-900 table-auto tbl">
                          <thead >
                              <tr className='bg-green-400'>
                                  <th>ردیف</th>
                                  <th>تاریخ</th>
                                  <th>چراغ</th>
                                  <th>نوع معلولیت </th>
                                  <th>تصویر گرفته شده</th>
                                  </tr>
                          </thead>
                          <tbody>

                              {

                                  results.length > 1 ? (
                                      results.map((item, index) => {
                                          return <tr key={index} className="border-collapse border-gray-700 ">
                                              <td className='text-center'>{index}</td>
                                               <td className='text-center'>{item.date2}</td>
                                               
                                               {/* <script>
                                                  var el = document.getElementById('content');
                                                  var content;
                                                  if  ({item.lightflag}==true) {
                                                      content = '<td> Green0</td> '
                                                  }
                                                  if  ({item.lightflag}==false) {
                                                      content = '<td> Red11</td> '
                                                  }
                                                  el.insertAdjacentHTML('afterbegin', content);
                                              </script> */}
                                              {item.lightflag ==true && <td><center><img src="1.png"  width={20}/></center></td>}
                                              {item.lightflag ==false &&  <td><center><img src="2.png"  width={20}/></center></td>}
                                                  
                                             
                                                          
                                              {item.classobj ==0 && <td className='text-center'>نابینا</td>}
                                              {item.classobj ==2 && <td className='text-center'>معلولیت پا</td>}
                                              {item.classobj ==4 && <td className='text-center'>ویلچر</td>}
                                              {item.classobj ==3 && <td className='text-center'>کهنسال</td>}
                                              {item.classobj ==1 && <td className='text-center'>کودک</td>}
                                              <td className='text-center'><div className='items-stretch ' ><center><img className='object-fill ' src={"http://localhost:8000" + item.img}  width={150}/></center></div></td>


                                              {/* <td>{`data:image/png;ba64,${item.img}`}</td> */}
                                              
                                              {/* <td><img src={"http://127.0.0.1:8000/detect" + item.img}/></td> */}
                                              {/* {console.log('image',`${item.img}`)} */}
                                               
                                              
                                          </tr>
                                      })) : <></>}

                          </tbody>
                      </table>
                  </div>
              </div>
          </div>
        </div>
     </div>)



            {/* <h1>First News</h1>
            <h1>The id is : {id}</h1> */}
        // </div>)
    }

    export default Report;