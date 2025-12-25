import { createClient } from "@/utils/supabase/server"
import { redirect } from "next/navigation"

export default async function Home() {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (user) redirect("/dashboard")

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-6xl font-bold mb-8">Supabase Pro E2E</h1>
      <a href="/auth/signin" className="bg-blue-500 text-white px-8 py-4 rounded-lg text-xl hover:bg-blue-600">
        Get Started
      </a>
    </main>
  )
}
