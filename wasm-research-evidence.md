# Raw Research Evidence: WASM in 2026

Sources gathered via curl from live websites on 22 July 2026.

---

## Source 1: webassembly.org — Use Cases (27 listed)

Retrieved from: https://webassembly.org/docs/use-cases/
Extraction method: grep for <li> tags

List of official use cases:
1. Image / video editing
2. Casual games that need to start quickly
3. AAA games that have heavy assets
4. Game portals (mixed-party/origin content)
5. Music applications (streaming, caching)
6. Image recognition
7. Live video augmentation
8. VR and augmented reality (very low latency)
9. CAD applications
10. Scientific visualization and simulation
11. Interactive educational software, and news articles
12. Platform simulation / emulation (ARC, DOSBox, QEMU, MAME, ...)
13. Language interpreters and virtual machines
14. POSIX user-space environment, allowing porting of existing POSIX applications
15. Developer tooling (editors, compilers, debuggers, ...)
16. Remote desktop
17. VPN
18. Encryption
19. Local web server
20. Common NPAPI users, within the web's security model and APIs
21. Fat client for enterprise applications (e.g. databases)
22. Server-side compute of untrusted code
23. Server-side application
24. Hybrid native apps on mobile devices
25. Symmetric computations across multiple nodes
26. Entire code base in WebAssembly
27. Main frame in WebAssembly, but the UI is in JavaScript / HTML

---

## Source 2: webassembly.org — FAQ

Retrieved from: https://webassembly.org/docs/faq/

Key quotes:

**"Is WebAssembly trying to replace JavaScript? No! WebAssembly is designed to be a complement to, not replacement of, JavaScript. While WebAssembly will, over time, allow many languages to be compiled to the Web, JavaScript has an incredible amount of momentum and will remain the single, privileged (as described above) dynamic language of the Web."**

Three expected configurations of JS + WASM:
1. "Whole, compiled C++ apps that leverage JavaScript to glue things together."
2. "HTML/CSS/JavaScript UI around a main WebAssembly-controlled center canvas, allowing developers to leverage the power of web frameworks to build accessible, web-native-feeling experiences."
3. "Mostly HTML/CSS/JavaScript app with a few high-performance WebAssembly modules (e.g., graphing, simulation, image/sound/video processing, visualization, animation, compression, etc.)"

Additional note: "When WebAssembly gains the ability to access garbage-collected objects, those objects will be shared with JavaScript, and not live in a walled-off world of their own."

Performance claim: "The kind of binary format being considered for WebAssembly can be natively decoded much faster than JavaScript can be parsed (experiments show more than 20x faster). On mobile, large compiled codes can easily take 20-40 seconds just to parse."

Architecture: "WebAssembly inside its existing JavaScript engine (thereby reusing the JavaScript engine's existing compiler backend, ES6 module loading frontend, security sandboxing mechanisms and other supporting VM components). Thus, in cost, WebAssembly should be comparable to a big new JavaScript feature."

---

## Source 3: Figma Blog

Retrieved from: https://www.figma.com/blog/webassembly-cut-figmas-load-time-by-3x/

Title: "WebAssembly cut Figma's load time by 3x"
Author: Evan Wallace, co-founder and former CTO at Figma

Content summary: Figma reported that WebAssembly reduced their product's load time by 3x. Their core rendering engine runs as compiled C++ via WASM, with the UI layer in JavaScript/HTML. This is a canonical production success story showing WASM + JS working together.

---

## Source 4: Cloudflare Workers Blog

Retrieved from: https://blog.cloudflare.com/tag/webassembly/

WASM-related blog post titles (extracted from tag page):
- "Making Rust Workers reliable: panic and abort recovery in wasm-bindgen"
- "Bringing Python to Workers using Pyodide and WebAssembly"
- "Wasm core dumps and debugging Rust in Cloudflare Workers"
- "Use the language of your choice with Pages Functions via WebAssembly"
- "Running Zig with WASI on Cloudflare Workers"
- "Announcing support for WASI on Cloudflare Workers"
- "Native Rust support on Cloudflare Workers"
- "Let's build a Cloudflare Worker with WebAssembly and Haskell"
- "Building a serverless, post-quantum Matrix homeserver"
- "We shipped FinalizationRegistry in Workers"

---

## Source 5: V8 (Google) Blog

Retrieved from: https://v8.dev/blog

WASM-related post titles:
- "Speculative Optimizations for WebAssembly using Deopts and Inlining"
- "Introducing the WebAssembly JavaScript Promise Integration API" (JSPI)
- "WebAssembly JSPI has a new API"
- "WebAssembly JSPI is going to origin trial"
- "A new way to bring garbage collected programming languages efficiently to WebAssembly" (WASM GC)
- "WebAssembly tail calls"
- "WebAssembly Dynamic Tiering ready to try in Chrome 96"
- "Up to 4GB of memory in WebAssembly"
- "Outside the web: standalone WebAssembly binaries using Emscripten"

---

## Source 6: webassembly.org — Homepage

Retrieved from: https://webassembly.org/

"WebAssembly (abbreviated Wasm) is a binary instruction format for a stack-based virtual machine. Wasm is designed as a portable compilation target for programming languages, enabling deployment on the web for client and server applications."

Key attributes:
- Efficient and fast: "aims to execute at native speed"
- Safe: "memory-safe, sandboxed execution environment"
- Open and debuggable: textual format for debugging
- Part of the open web platform: "WebAssembly modules will be able to call into and out of the JavaScript context and access browser functionality through the same Web APIs accessible from JavaScript"
