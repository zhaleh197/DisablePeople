"use client";
import React, { useState, useEffect } from "react";
var L = "Red";

const Videoload = ({ socket }) => {
  const [frame, setframe] = useState("");
  const [results, setresults] = useState([]);
  console.log("result", results);
  useEffect(() => {
    while (true) {
      socket.emit("request-frame", {});

      socket.on("new-frame", (data) => {
        setframe(data.base64);
        // console.log(typeof(data.rec))
        if (data.rec != null) {
          // setframe(data.rec["main_image"])
          //   console.log(data.rec);
          if (results.length > 5) {
            setresults(results.slice(results.length - 5, results.length - 1));
          } else {
            setresults([...results, data.rec]);
          }
        }
      });

      return () => {
        socket.off("new-frame", () => {
          console.log("first");
        });
      };
    }
  }, [socket, results, frame]);

  return (
    <div>
      <div className="flex">
        <div className="h-[320px] bg-black w-[640px] mx-auto  ">
          <div>
            <img
              src={`data:image/jpeg;base64,${frame}`}
              alt=""
              className="w-full h-[320px]"
            />
          </div>
        </div>
        <div className=" ">
          {results.map((element) => {
            return (
              <div className="h-40 w-40 absolute top-52 left-12" key={element.id}>
                {element.lightflag ? (
                  <img className="h-full w-full" src="/red.jpg" />
                ) : (
                  <img className="h-full w-full" src="/green.jpg" />
                )}
              </div>
            );
          })}
        </div>
        {/* <div className="h-32 ml-4 w-32">
          <img id="targetdiv" className=" " src="/green.jpg" />
        </div> */}
      </div>
      {/* <div  dir="rtl" className=' '>
                    <table className='table-auto'>
                    <thead >
                        <tr className='justify-around'>
                        <td className=''><div className=' w-auto' ><div className='h-[480px] bg-black w-[750px] m-16 relative'>

</div></div> </td><div width="900" height="500" className='w-80'></div>             
                        <td  className="object-left " ><div  >
                        <center><img id="targetdiv" className='object-fill ' src="\green.jpg"  width={300}/>
                        {/* {results.map((item, index) =>item.lightflag ==true) && <td><center><img className='object-fill ' src="\green.jpg"  width={300}/></center></td>}
                        {results.map((item, index) =>item.lightflag ==false) &&  <td><center><img className='object-fill ' src="\red.jpg"  width={300}/></center></td>} */}
      {/* </center>  */}

      {/* // </div></td></tr></thead ></table></div>  */}

      <div className="flex flex-col border-2 h-[300px] overflow-x-hidden mt-4">
        <div className="overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="py-2 inline-block min-w-full sm:px-6 lg:px-8">
            <div className="overflow-hidden">
              <table className="min-w-full table-auto tbl">
                <thead>
                  <tr>
                    <th>ردیف</th>
                    <th>تاریخ</th>
                    <th>چراغ</th>
                    <th>نوع معلولیت </th>
                    <th>تصویر گرفته شده</th>
                  </tr>
                </thead>
                <tbody>
                  {results.length > 1 ? (
                    results.map((item, index) => {
                      if (item.classobj != null) {
                        return (
                          <tr key={index} className="border-2 border-gray-200">
                            <td>{index}</td>
                            <td>{item.date_created}</td>

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
                                                    // </script> */}
                            {/* // {item.lightflag ==true && <td>Green</td>}
                                                    // {item.lightflag ==false && <td>Red</td>} */}

                            {item.lightflag == true && (
                              <td>
                                <center>
                                  <img src="\1.png" width={20} />
                                </center>
                              </td>
                            )}
                            {item.lightflag == false && (
                              <td>
                                <center>
                                  <img src="\2.png" width={20} />
                                </center>
                              </td>
                            )}
                            {item.classobj == 0 && (
                              <td className="text-center">نابینا</td>
                            )}
                            {item.classobj == 2 && (
                              <td className="text-center">معلولیت پا</td>
                            )}
                            {item.classobj == 4 && (
                              <td className="text-center">ویلچر</td>
                            )}
                            {item.classobj == 3 && (
                              <td className="text-center">کهنسال</td>
                            )}
                            {item.classobj == 1 && (
                              <td className="text-center">کودک</td>
                            )}

                            {/* <td className='text-center'><div className='items-stretch ' ><center><img className='object-fill ' src={"http://localhost:8000" + item.img}  width={150}/></center></div></td> */}

                            {/* <td>{`data:image/png;base64,${item.img}`}</td> */}
                            <td>
                              <center>
                                <img
                                  src={`data:image/png;base64,${item.img}`}
                                  width={100}
                                />
                              </center>
                            </td>
                            {/* <td><img src={"http://127.0.0.1:8000/detect" + item.img}/></td> */}
                            {/* {console.log('image',`${item.img}`)} */}

                            {/* {item.flag : <img /> ? <img />} */}
                            {/* {item.lightflag ==true && <td><center><img className='object-fill ' src="\green.jpg"  width={300}/></center></td>}
                                                {item.lightflag ==false &&  <td><center><img className='object-fill ' src="\red.jpg"  width={300}/></center></td>} */}
                          </tr>
                        );
                      }
                      // document.getElementById('targetdiv').src="\red.jpg"
                    })
                  ) : (
                    <></>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
    
  );
};

export default Videoload;
