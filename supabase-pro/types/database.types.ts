// Supabase Pro E2E - Generated Types for sbp_5e354f2c96f18b94c9ac03e992560fca7073c2f7
// Run: npx supabase gen types typescript --project-id sbp_5e354f2c96f18b94c9ac03e992560fca7073c2f7

export type Json = string | number | boolean | null | { [key: string]: Json } | Json[]

export interface Database {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string
          username: string | null
          website: string | null
          bio: string | null
          created_at: string
        }
        Insert: {
          id: string
          username?: string | null
          website?: string | null
          bio?: string | null
          created_at?: string
        }
        Update: {
          id?: string
          username?: string | null
          website?: string | null
          bio?: string | null
          created_at?: string
        }
      }
      posts: {
        Row: {
          id: string
          user_id: string
          title: string
          content: string | null
          published: boolean
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          user_id: string
          title: string
          content?: string | null
          published?: boolean
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          title?: string
          content?: string | null
          published?: boolean
          created_at?: string
          updated_at?: string
        }
      }
      users: {
        Row: {
          id: string
          email: string
          full_name: string | null
          avatar_url: string | null
          phone: string | null
          metadata: Json | null
          email_confirmed_at: string | null
          phone_confirmed_at: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id: string
          email: string
          full_name?: string | null
          avatar_url?: string | null
          phone?: string | null
          metadata?: Json | null
          email_confirmed_at?: string | null
          phone_confirmed_at?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          email?: string
          full_name?: string | null
          avatar_url?: string | null
          phone?: string | null
          metadata?: Json | null
          email_confirmed_at?: string | null
          phone_confirmed_at?: string | null
          created_at?: string
          updated_at?: string
        }
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
  }
}
