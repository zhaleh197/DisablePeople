import Cookies from "js-cookie";
import { NextResponse } from "next/server";

export default async function middleware(req, res) {
  const token = req.cookies.get("token");
  if (!token && req.nextUrl.pathname.startsWith("/admin/")) {
    return NextResponse.redirect("http://localhost:3000/");
  }
  if (!token && req.nextUrl.pathname.startsWith("/admin")) {
    return NextResponse.redirect("http://localhost:3000/");
  }
  if (token && req.nextUrl.pathname.startsWith("/login")) {
    return NextResponse.redirect("http://localhost:3000/admin/main");
  }
}
