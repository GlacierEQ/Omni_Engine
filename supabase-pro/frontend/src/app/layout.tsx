import { createClient } from "@/utils/supabase/server"
import { cookies } from "next/headers"
import { redirect } from "next/navigation"
import { ReactNode } from "react"

export default async function RootLayout({ children }: { children: ReactNode }) {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
