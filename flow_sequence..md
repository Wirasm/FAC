┌──────┐          ┌───────┐          ┌───────┐          ┌────────┐
│ User │          │ Astro │          │ Clerk │          │ FastAPI│
│      │          │       │          │       │          │        │
└──┬───┘          └───┬───┘          └───┬───┘          └────┬───┘
   │                  │                  │                    │
   │  Visit Website   │                  │                    │
   │─────────────────>│                  │                    │
   │                  │                  │                    │
   │                  │   Load Clerk JS  │                    │
   │                  │─────────────────>│                    │
   │                  │                  │                    │
   │                  │  Clerk JS Loaded │                    │
   │                  │<─────────────────│                    │
   │                  │                  │                    │
   │  Sign-in Action  │                  │                    │
   │─────────────────>│                  │                    │
   │                  │                  │                    │
   │                  │ Authentication   │                    │
   │                  │ Request          │                    │
   │                  │─────────────────>│                    │
   │                  │                  │                    │
   │                  │ Authentication   │                    │
   │                  │ Response + JWT   │                    │
   │                  │<─────────────────│                    │
   │                  │                  │                    │
   │ Protected Page   │                  │                    │
   │ Request          │                  │                    │
   │─────────────────>│                  │                    │
   │                  │                  │                    │
   │                  │ Request Protected│                    │
   │                  │ API Data with JWT│                    │
   │                  │────────────────────────────────────────>│
   │                  │                  │                    │
   │                  │                  │                    │
   │                  │                  │ Verify JWT Token   │
   │                  │                  │<───────────────────│
   │                  │                  │                    │
   │                  │                  │ JWT Verification   │
   │                  │                  │ Response           │
   │                  │                  │───────────────────>│
   │                  │                  │                    │
   │                  │ Protected Data   │                    │
   │                  │ Response         │                    │
   │                  │<───────────────────────────────────────│
   │                  │                  │                    │
   │ Protected Page   │                  │                    │
   │ with Data        │                  │                    │
   │<─────────────────│                  │                    │
   │                  │                  │                    │