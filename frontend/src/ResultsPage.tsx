import { Link, useLocation } from "react-router"
import { motion } from "motion/react"
import SimilarityChart from "./components/SimilarityChart"

type CitationResponse = {
  file_path: string
  start_line: number | null
  end_line: number | null
  similarity_score: number
}

type AnswerStep = {
  title: string
  explanation: string
  citation: string
}

type ParsedAnswer = {
  summary: string
  steps: AnswerStep[]
}

type ResultsPageState = {
  answer: string
  citations: CitationResponse[]
  question: string
  repositoryId: number
  repositoryName: string
}

function parseAnswer(answerText: string): ParsedAnswer {
  const normalizedAnswer = answerText.replace(/\r\n/g, "\n")

  const summaryMatch = normalizedAnswer.match(
    /SUMMARY:\s*([\s\S]*?)(?=\n\s*STEP:|$)/,
  )

  const stepBlocks = normalizedAnswer
    .split(/\n\s*STEP:\s*/)
    .slice(1)

  const steps = stepBlocks
    .map((block): AnswerStep | null => {
      const citationMatch = block.match(
        /\n\s*CITATION:\s*(\[[^\]\n]+\])\s*$/,
      )

      if (!citationMatch) {
        return null
      }

      const contentWithoutCitation = block
        .slice(0, citationMatch.index)
        .trim()

      const [titleLine, ...explanationLines] =
        contentWithoutCitation.split("\n")

      return {
        title: titleLine.trim(),
        explanation: explanationLines.join("\n").trim(),
        citation: citationMatch[1].trim(),
      }
    })
    .filter((step): step is AnswerStep => step !== null)

  return {
    summary: summaryMatch?.[1].trim() ?? "",
    steps,
  }
}

const stepStyles = [
  {
    heading: "from-blue-500 to-cyan-400",
    number: "from-blue-500 to-cyan-400",
    citation:
      "border-blue-400/20 bg-blue-400/10 text-blue-200",
    line: "from-blue-400 via-cyan-400 to-transparent",
  },
  {
    heading: "from-emerald-500 to-teal-400",
    number: "from-emerald-500 to-teal-400",
    citation:
      "border-emerald-400/20 bg-emerald-400/10 text-emerald-200",
    line:
      "from-emerald-400 via-teal-400 to-transparent",
  },
  {
    heading: "from-violet-500 to-fuchsia-400",
    number: "from-violet-500 to-fuchsia-400",
    citation:
      "border-violet-400/20 bg-violet-400/10 text-violet-200",
    line:
      "from-violet-400 via-fuchsia-400 to-transparent",
  },
  {
    heading: "from-amber-500 to-orange-400",
    number: "from-amber-500 to-orange-400",
    citation:
      "border-amber-400/20 bg-amber-400/10 text-amber-200",
    line:
      "from-amber-400 via-orange-400 to-transparent",
  },
  {
    heading: "from-rose-500 to-pink-400",
    number: "from-rose-500 to-pink-400",
    citation:
      "border-rose-400/20 bg-rose-400/10 text-rose-200",
    line:
      "from-rose-400 via-pink-400 to-transparent",
  },
]

function ResultsPage() {
  const location = useLocation()
  const state = location.state as ResultsPageState | null

  if (!state) {
    return (
      <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[#050816] px-6 text-white">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(59,130,246,0.16),_transparent_48%)]" />

        <motion.div
          className="relative max-w-md rounded-3xl border border-white/10 bg-slate-900/80 p-8 text-center shadow-2xl shadow-black/40 backdrop-blur"
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
        >
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-400 font-bold text-white">
            AI
          </div>

          <h1 className="mt-6 text-2xl font-bold">
            No answer available
          </h1>

          <p className="mt-3 text-slate-400">
            Ask a repository question before opening this page.
          </p>

          <Link
            to="/"
            className="mt-6 inline-flex rounded-xl bg-blue-500 px-5 py-3 font-semibold text-white transition hover:bg-blue-400"
          >
            Return home
          </Link>
        </motion.div>
      </main>
    )
  }

  const parsedAnswer = parseAnswer(state.answer)

  return (
    <motion.main
      className="relative min-h-screen overflow-hidden bg-[#050816] text-white"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.45 }}
    >
      {/* Static radial glow */}
      <div className="pointer-events-none fixed inset-0 bg-[radial-gradient(circle_at_top,_rgba(59,130,246,0.14),_transparent_48%)]" />

      {/* Lightweight moving grid */}
      <motion.div
        className="pointer-events-none fixed inset-0 opacity-[0.08]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(148,163,184,0.16) 1px, transparent 1px), linear-gradient(90deg, rgba(148,163,184,0.16) 1px, transparent 1px)",
          backgroundSize: "48px 48px",
        }}
        animate={{
          backgroundPosition: [
            "0px 0px",
            "48px 48px",
          ],
        }}
        transition={{
          duration: 28,
          repeat: Infinity,
          ease: "linear",
        }}
      />

      <div className="relative z-10">
        <motion.header
          className="border-b border-white/10 bg-[#050816]/85 backdrop-blur"
          initial={{ y: -24, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{
            duration: 0.45,
            ease: "easeOut",
          }}
        >
          <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
            <div className="flex items-center gap-3">
              <motion.div
                className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 font-bold text-white"
                whileHover={{ scale: 1.06 }}
                transition={{ duration: 0.18 }}
              >
                AI
              </motion.div>

              <div>
                <p className="font-bold">
                  Codebase Assistant
                </p>

                <p className="text-sm text-slate-400">
                  {state.repositoryName}
                </p>
              </div>
            </div>

            <motion.div
              whileHover={{ scale: 1.025 }}
              whileTap={{ scale: 0.98 }}
            >
              <Link
                to="/"
                className="rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-sm font-semibold text-slate-200 transition hover:border-blue-400/40 hover:bg-blue-400/10 hover:text-white"
              >
                Ask another question
              </Link>
            </motion.div>
          </div>
        </motion.header>

        <div className="mx-auto max-w-7xl px-6 py-12">
          <motion.section
            className="mb-8 flex items-start gap-4"
            initial={{ opacity: 0, x: -28 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{
              duration: 0.5,
              delay: 0.1,
              ease: "easeOut",
            }}
          >
            <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-violet-500 text-xl font-bold text-white">
              {parsedAnswer.steps.length}
            </div>

            <div>
              <h1 className="bg-gradient-to-r from-white via-blue-100 to-cyan-300 bg-clip-text text-2xl font-bold tracking-tight text-transparent sm:text-3xl">
                Numbered codebase explanation
              </h1>

              <p className="mt-1 text-slate-400">
                Step-by-step answer with direct file and line citations.
              </p>

              <div className="mt-4 rounded-xl border border-white/10 bg-white/5 px-4 py-3">
                <p className="text-xs font-bold uppercase tracking-[0.18em] text-blue-300">
                  Question
                </p>

                <p className="mt-1 text-sm font-medium text-slate-200">
                  {state.question}
                </p>
              </div>
            </div>
          </motion.section>

          <motion.section
            className="overflow-hidden rounded-3xl border border-white/10 bg-slate-900/70 shadow-2xl shadow-black/30 backdrop-blur"
            initial={{ opacity: 0, y: 28 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              duration: 0.5,
              delay: 0.18,
              ease: "easeOut",
            }}
          >
            {parsedAnswer.summary && (
              <motion.div
                className="m-6 rounded-2xl border border-cyan-400/20 bg-gradient-to-br from-cyan-400/10 via-blue-400/10 to-violet-400/10 px-6 py-5"
                initial={{ opacity: 0, y: 18 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{
                  duration: 0.45,
                  delay: 0.28,
                }}
                whileHover={{
                  y: -2,
                  borderColor: "rgba(34,211,238,0.35)",
                }}
              >
                <div className="flex items-start gap-4">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-cyan-400/15 text-xl text-cyan-300">
                    ✦
                  </div>

                  <div>
                    <h2 className="font-bold text-cyan-200">
                      Summary
                    </h2>

                    <p className="mt-2 max-w-5xl leading-7 text-slate-300">
                      {parsedAnswer.summary}
                    </p>
                  </div>
                </div>
              </motion.div>
            )}

            {parsedAnswer.steps.length > 0 ? (
              <div className="px-6 pb-4">
                {parsedAnswer.steps.map((step, index) => {
                  const style =
                    stepStyles[index % stepStyles.length]

                  const citationText = step.citation
                    .replace("[", "")
                    .replace("]", "")

                  const separatorIndex =
                    citationText.lastIndexOf(":")

                  const citationFile =
                    separatorIndex >= 0
                      ? citationText.slice(0, separatorIndex)
                      : citationText

                  const citationLines =
                    separatorIndex >= 0
                      ? citationText.slice(
                          separatorIndex + 1,
                        )
                      : ""

                  return (
                    <motion.article
                      key={`${step.title}-${index}`}
                      className="relative grid gap-6 border-b border-white/10 py-8 last:border-b-0 md:grid-cols-[64px_minmax(0,1fr)_260px]"
                      initial={{
                        opacity: 0,
                        y: 22,
                      }}
                      animate={{
                        opacity: 1,
                        y: 0,
                      }}
                      transition={{
                        duration: 0.42,
                        delay: 0.3 + index * 0.07,
                        ease: "easeOut",
                      }}
                    >
                      <div className="relative flex justify-center">
                        {index <
                          parsedAnswer.steps.length - 1 && (
                          <div
                            className={`absolute left-1/2 top-11 h-[calc(100%+32px)] w-[2px] -translate-x-1/2 bg-gradient-to-b ${style.line}`}
                          />
                        )}

                        <motion.div
                          className={`relative z-10 flex h-11 w-11 items-center justify-center rounded-full bg-gradient-to-br text-sm font-bold text-white ${style.number}`}
                          initial={{ scale: 0.8, opacity: 0 }}
                          animate={{ scale: 1, opacity: 1 }}
                          transition={{
                            duration: 0.3,
                            delay: 0.36 + index * 0.07,
                          }}
                          whileHover={{
                            scale: 1.07,
                          }}
                        >
                          {String(index + 1).padStart(
                            2,
                            "0",
                          )}
                        </motion.div>
                      </div>

                      <motion.div
                        className="min-w-0 rounded-2xl border border-white/10 bg-white/[0.035] p-5"
                        whileHover={{
                          borderColor:
                            "rgba(96,165,250,0.32)",
                          backgroundColor:
                            "rgba(255,255,255,0.05)",
                        }}
                        transition={{ duration: 0.18 }}
                      >
                        <div
                          className={`rounded-xl bg-gradient-to-r px-4 py-3 text-white ${style.heading}`}
                        >
                          <h2 className="text-lg font-bold">
                            {step.title}
                          </h2>
                        </div>

                        <div className="mt-5 space-y-3 leading-7 text-slate-300">
                          {step.explanation
                            .split("\n")
                            .filter(
                              (line) =>
                                line.trim() !== "",
                            )
                            .map((line, lineIndex) => (
                              <p
                                key={`${step.title}-${lineIndex}`}
                              >
                                {line}
                              </p>
                            ))}
                        </div>
                      </motion.div>

                      <motion.div
                        className={`h-fit rounded-2xl border px-4 py-4 ${style.citation}`}
                        initial={{
                          opacity: 0,
                          x: 18,
                        }}
                        animate={{
                          opacity: 1,
                          x: 0,
                        }}
                        transition={{
                          duration: 0.35,
                          delay: 0.38 + index * 0.07,
                        }}
                        whileHover={{
                          y: -2,
                          scale: 1.01,
                        }}
                      >
                        <p className="text-xs font-bold uppercase tracking-[0.16em] opacity-70">
                          Citation
                        </p>

                        <p className="mt-3 break-all font-mono text-sm font-bold leading-6">
                          {citationFile}
                        </p>

                        {citationLines && (
                          <p className="mt-2 font-mono text-sm font-semibold opacity-80">
                            lines {citationLines}
                          </p>
                        )}
                      </motion.div>
                    </motion.article>
                  )
                })}
              </div>
            ) : (
              <div className="px-6 pb-6">
                <div className="rounded-xl border border-amber-400/20 bg-amber-400/10 p-5">
                  <p className="font-semibold text-amber-200">
                    The response did not follow the structured answer
                    format.
                  </p>
                </div>

                <pre className="mt-5 overflow-x-auto whitespace-pre-wrap rounded-xl border border-white/10 bg-black/40 p-6 font-mono text-sm leading-7 text-slate-200">
                  <code>{state.answer}</code>
                </pre>
              </div>
            )}
          </motion.section>

          {state.citations.length > 0 && (
            <div className="mt-8">
              <SimilarityChart citations={state.citations} />
            </div>
          )}
          
          {state.citations.length > 0 && (
            <motion.section
              className="mt-8 rounded-3xl border border-white/10 bg-slate-900/70 p-6 shadow-2xl shadow-black/20 backdrop-blur"
              initial={{ opacity: 0, y: 28 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                duration: 0.45,
                delay: 0.4,
              }}
            >
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h2 className="text-lg font-bold text-white">
                    Retrieved citation list
                  </h2>

                  <p className="mt-1 text-sm text-slate-400">
                    All source chunks returned by semantic search.
                  </p>
                </div>

                <span className="w-fit rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 text-sm font-semibold text-cyan-200">
                  {state.citations.length} sources
                </span>
              </div>

              <div className="mt-6 grid gap-3 sm:grid-cols-2">
                {state.citations.map(
                  (citation, index) => (
                    <motion.div
                      key={`${citation.file_path}-${citation.start_line}-${citation.end_line}-${index}`}
                      className="rounded-2xl border border-white/10 bg-white/[0.035] px-4 py-4"
                      initial={{
                        opacity: 0,
                        y: 16,
                      }}
                      animate={{
                        opacity: 1,
                        y: 0,
                      }}
                      transition={{
                        duration: 0.32,
                        delay: 0.45 + index * 0.04,
                      }}
                      whileHover={{
                        y: -2,
                        borderColor:
                          "rgba(34,211,238,0.3)",
                      }}
                    >
                      <div className="flex gap-3">
                        <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-blue-500 to-cyan-400 text-xs font-bold text-white">
                          {index + 1}
                        </span>

                        <div className="min-w-0">
                          <p className="break-all font-mono text-sm font-semibold text-cyan-300">
                            {citation.file_path}
                          </p>

                          <p className="mt-1 font-mono text-xs text-slate-500">
                            Lines{" "}
                            {citation.start_line ??
                              "unknown"}
                            –
                            {citation.end_line ??
                              "unknown"}
                          </p>
                        </div>
                      </div>
                    </motion.div>
                  ),
                )}
              </div>
            </motion.section>
          )}
        </div>
      </div>
    </motion.main>
  )
}

export default ResultsPage