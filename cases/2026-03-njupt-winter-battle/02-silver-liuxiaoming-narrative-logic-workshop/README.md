- # Interactive Narrative & Logic Workshop

  [中文版本](./README_ZH.md)

  ## Project Overview 

  This project is an AI-powered co-writing platform designed for novelists. Beyond mere text generation, it introduces the concept of "Narrative Auditing," utilizing LLMs to monitor logical consistency and evaluate structural integrity in real-time. 

  - **Problem Solved**: Addresses common writing pitfalls such as plot holes, character inconsistency, and poor pacing in long-form narratives. 
  - **Core Value**: Transforms AI from a simple generator into a "Virtual Editor" with logical intuition.

  ## Activity Information 

  - **Competition / Workshop:** 2026 NJUPT Winter Battle 
  - **Team Members:** Liu Xiaoming, Teng mingyan 
  - **Awarded:** Silver

  ## Environment 

  - **Base Image:** Basic GPU Environment (aup-learning-cloud)
  - **Extra Dependencies:** Listed in `requirements.txt` 

  ## Quick Start 

  1. In aup-learning-cloud, select **Basic GPU Environment** and set the Git URL to this repository
  2. Navigate to `cases/2026-03-njupt-winter-battle/liuxiaoming-narrative-logic-workshop`
  3. Open `main.ipynb`
  4. Run all cells from top to bottom
  5. Enter a plot segment in the "Continue the story here..." box, then click any button below to test the tool
  ## Technical Highlights

  The workshop utilizes a **Frontend-Logic-Backend** asynchronous architecture to ensure a smooth UI experience during high-latency LLM inference. 

  ```mermaid
  sequenceDiagram
      participant User as User (ipywidgets)
      participant Logic as Logic Layer (Python)
      participant AMD as AMD ROCm Backend (Qwen3)
      
      User->>Logic: Input plot/instruction
      Logic->>Logic: Context Truncation (Head-Tail)
      Logic->>AMD: Optimized Prompt (CoT/Few-shot)
      AMD-->>Logic: Generated Content / Analysis
      Logic-->>User: Async UI Update
  ```

  1. **32k Context Management**: Implemented a "Head-Tail Anchor Strategy" to preserve essential world-building (Head) and recent plot development (Tail), ensuring coherence within hardware limits.
  2. **Consistency Auditing**: Uses Chain-of-Thought (CoT) prompting to guide the model through logical cross-referencing of the last 5000 characters.
  3. **Three-Act Analysis**: Applies literary theory to provide automated structural diagnostics and pacing scores.
  4. **Error Handling & UX**: Features multi-threaded "Anti-freeze" UI and a hardware-level `Stop` button for robust API interaction.

  ## Results / Demo

    ![](image/N1BGsyde_converted.gif)

  1. **Story Input & Continuation**
      ![](./image/213617.png)
      ![](./image/214033.png)
      2.**Consistency Check Test**
      ![](./image/214226.png)
      ![](./image/214241.png)
      3.**Structural Analysis Test**
      ![](./image/214317.png)
      ![](./image/214327.png)
      4.**Minimal Input Generation (Opening + Short Prompt)**
      ![](./image/214625.png)
      ![](./image/214645.png)
  ## References

  - [AMD ROCm Documentation](https://rocm.docs.amd.com/)
  - [Qwen3 Model Repository](https://github.com/QwenLM/Qwen)
  - [Three-Act Structure Theory](https://en.wikipedia.org/wiki/Three-act_structure)
  - [The Universe Is Not Happening](https://tw.z-library.sk/book/ZjKamZMXO0/%E5%AE%87%E5%AE%99%E6%97%A0%E4%BA%8B%E5%8F%91%E7%94%9F.html)

- https://tw.z-library.sk/book/ZjKamZMXO0/%E5%AE%87%E5%AE%99%E6%97%A0%E4%BA%8B%E5%8F%91%E7%94%9F.html)

