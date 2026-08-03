import { useState } from "react"
import { motion } from "framer-motion";
import {
  Route,
  Routes,
  useNavigate,
} from "react-router"

import ResultsPage from "./ResultsPage"

type RepositoryResponse = {
  id: number
  github_url: string
  name: string
  owner: string
  default_branch: string
  latest_commit_sha: string | null
  ingestion_status: string
}

type CitationResponse = {
  file_path: string
  start_line: number | null
  end_line: number | null
}

type QuestionResponse = {
  answer: string
  citations: CitationResponse[]
}

function HomePage() {
  const navigate = useNavigate()

  const [githubUrl, setGithubUrl] = useState("")
  const [repository, setRepository] =
    useState<RepositoryResponse | null>(null)

  const [isLoading, setIsLoading] = useState(false)
  const [repositoryError, setRepositoryError] = useState("")

  const [repositories, setRepositories] = useState<
    RepositoryResponse[]
  >([])

  const [
    isLoadingRepositories,
    setIsLoadingRepositories,
  ] = useState(false)

  const [showRepositories, setShowRepositories] =
    useState(false)

  const [question, setQuestion] = useState("")
  const [isAsking, setIsAsking] = useState(false)
  const [questionError, setQuestionError] = useState("")

  const activeRepositoryId = repository?.id ?? null

  async function handleRepositorySubmit(
    event: React.SubmitEvent<HTMLFormElement>,
  ) {
    event.preventDefault()

    setIsLoading(true)
    setRepositoryError("")
    setRepository(null)
    setQuestion("")
    setQuestionError("")

    try {
      const response = await fetch(
        "http://localhost:5001/repositories",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            github_url: githubUrl,
          }),
        },
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.detail ?? "Repository ingestion failed.",
        )
      }

      setRepository(data as RepositoryResponse)
      setShowRepositories(false)
    } catch (error) {
      if (error instanceof Error) {
        setRepositoryError(error.message)
      } else {
        setRepositoryError(
          "An unexpected error occurred.",
        )
      }
    } finally {
      setIsLoading(false)
    }
  }

  async function handleOpenRepositories() {
    setIsLoadingRepositories(true)
    setRepositoryError("")

    try {
      const response = await fetch(
        "http://localhost:5001/repositories",
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.detail ?? "Unable to load repositories.",
        )
      }

      setRepositories(data as RepositoryResponse[])
      setShowRepositories(true)
    } catch (error) {
      if (error instanceof Error) {
        setRepositoryError(error.message)
      } else {
        setRepositoryError(
          "An unexpected error occurred.",
        )
      }
    } finally {
      setIsLoadingRepositories(false)
    }
  }

  function handleRepositorySelection(
    selectedRepository: RepositoryResponse,
  ) {
    setRepository(selectedRepository)
    setRepositoryError("")
    setQuestion("")
    setQuestionError("")
    setShowRepositories(false)
  }

  async function handleQuestionSubmit(
    event: React.SubmitEvent<HTMLFormElement>,
  ) {
    event.preventDefault()

    if (activeRepositoryId === null) {
      setQuestionError("Select a repository first.")
      return
    }

    setIsAsking(true)
    setQuestionError("")

    try {
      const response = await fetch(
        `http://localhost:5001/repositories/${activeRepositoryId}/questions`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question,
          }),
        },
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.detail ?? "Unable to answer the question.",
        )
      }

      const questionResponse = data as QuestionResponse

      navigate("/results", {
        state: {
          answer: questionResponse.answer,
          citations: questionResponse.citations,
          question,
          repositoryId: activeRepositoryId,
          repositoryName: repository
            ? `${repository.owner}/${repository.name}`
            : `Repository #${activeRepositoryId}`,
        },
      })
    } catch (error) {
      if (error instanceof Error) {
        setQuestionError(error.message)
      } else {
        setQuestionError(
          "An unexpected error occurred.",
        )
      }
    } finally {
      setIsAsking(false)
    }
  }

  return (
    <main className="relative min-h-screen overflow-hidden bg-slate-950 text-white">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(59,130,246,0.2),_transparent_42%)]" />
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        {/* Morphing cyan blob */}
        <motion.div
          className="absolute left-[-12rem] top-[8%] h-[38rem] w-[38rem] bg-gradient-to-br from-cyan-400/40 via-blue-500/30 to-purple-500/30 mix-blend-screen"
          animate={{
            x: [0, 340, 120, -80, 0],
            y: [0, 140, 360, 180, 0],
            scale: [1, 1.35, 0.9, 1.2, 1],
            rotate: [0, 90, 180, 270, 360],
            skewX: [0, 10, -8, 6, 0],
            borderRadius: [
              "50% 50% 50% 50%",
              "65% 35% 55% 45%",
              "35% 65% 40% 60%",
              "55% 45% 70% 30%",
              "50% 50% 50% 50%",
            ],
            opacity: [0.25, 0.7, 0.4, 0.6, 0.25],
            filter: [
              "blur(80px) brightness(1)",
              "blur(120px) brightness(1.5)",
              "blur(90px) brightness(1)",
              "blur(110px) brightness(1.3)",
              "blur(80px) brightness(1)",
            ],
          }}
          transition={{
            duration: 24,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />

        {/* Morphing purple blob */}
        <motion.div
          className="absolute right-[-14rem] top-[4%] h-[42rem] w-[42rem] bg-gradient-to-br from-blue-500/30 via-violet-500/40 to-fuchsia-500/30 mix-blend-screen"
          animate={{
            x: [0, -420, -160, 120, 0],
            y: [0, 220, 40, 320, 0],
            scale: [1, 0.85, 1.35, 1.1, 1],
            rotate: [360, 260, 160, 80, 0],
            skewY: [0, -10, 8, -5, 0],
            borderRadius: [
              "50% 50% 50% 50%",
              "40% 60% 70% 30%",
              "70% 30% 45% 55%",
              "30% 70% 60% 40%",
              "50% 50% 50% 50%",
            ],
            opacity: [0.2, 0.65, 0.35, 0.6, 0.2],
            filter: [
              "blur(90px) brightness(1)",
              "blur(125px) brightness(1.4)",
              "blur(85px) brightness(0.9)",
              "blur(115px) brightness(1.35)",
              "blur(90px) brightness(1)",
            ],
          }}
          transition={{
            duration: 28,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />

        {/* Rotating aurora */}
        <motion.div
          className="absolute left-1/2 top-1/2 h-[70rem] w-[70rem] -translate-x-1/2 -translate-y-1/2 rounded-full bg-[conic-gradient(from_0deg,transparent,rgba(34,211,238,0.2),transparent,rgba(168,85,247,0.25),transparent,rgba(59,130,246,0.2),transparent)] blur-[110px] mix-blend-screen"
          animate={{
            rotate: [0, 360],
            scale: [0.8, 1.15, 0.9, 0.8],
            opacity: [0.2, 0.5, 0.3, 0.2],
          }}
          transition={{
            rotate: {
              duration: 40,
              repeat: Infinity,
              ease: "linear",
            },
            scale: {
              duration: 14,
              repeat: Infinity,
              ease: "easeInOut",
            },
            opacity: {
              duration: 10,
              repeat: Infinity,
              ease: "easeInOut",
            },
          }}
        />

        {/* Faint pulsing center glow */}
        <motion.div
          className="absolute left-1/2 top-1/2 h-[28rem] w-[28rem] -translate-x-1/2 -translate-y-1/2 rounded-full bg-white/10 blur-[100px]"
          animate={{
            scale: [0.7, 1.4, 0.9, 0.7],
            opacity: [0.05, 0.25, 0.12, 0.05],
          }}
          transition={{
            duration: 9,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      </div>
      <div className="relative mx-auto flex min-h-screen max-w-6xl flex-col px-6">
        <header className="flex items-center justify-between border-b border-slate-800/70 py-6">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 font-bold shadow-lg shadow-blue-500/20">
              AI
            </div>

            <div>
              <p className="font-semibold tracking-tight">
                Codebase Assistant
              </p>

              <p className="text-xs text-slate-500">
                Repository intelligence
              </p>
            </div>
          </div>

          <div className="hidden items-center gap-2 rounded-full border border-slate-800 bg-slate-900/70 px-4 py-2 text-xs text-slate-400 sm:flex">
            <span className="h-2 w-2 rounded-full bg-emerald-400" />
            AI-powered code search
          </div>
        </header>

        <section className="py-16 text-center">
          <div className="mx-auto max-w-3xl">
            <div className="mb-6 inline-flex rounded-full border border-blue-400/20 bg-blue-400/10 px-4 py-2 text-sm text-blue-300">
              Understand unfamiliar codebases faster
            </div>

            <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
              Ask questions about any
              <span className="block bg-gradient-to-r from-blue-400 via-cyan-300 to-blue-400 bg-clip-text text-transparent">
                GitHub repository
              </span>
            </h1>

            <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-400">
              Analyze a public repository and receive grounded
              answers with direct file and line citations.
            </p>

            <div className="mx-auto mt-10 max-w-2xl rounded-3xl border border-slate-800 bg-slate-900/80 p-3 shadow-2xl shadow-black/30 backdrop-blur">
              <form
                onSubmit={handleRepositorySubmit}
                className="flex flex-col gap-3 sm:flex-row"
              >
                <label
                  htmlFor="github-url"
                  className="sr-only"
                >
                  GitHub repository URL
                </label>

                <input
                  id="github-url"
                  type="url"
                  value={githubUrl}
                  onChange={(event) =>
                    setGithubUrl(event.target.value)
                  }
                  placeholder="https://github.com/owner/repository"
                  required
                  disabled={isLoading}
                  className="min-w-0 flex-1 rounded-2xl border border-slate-700 bg-slate-950 px-5 py-4 text-white outline-none transition placeholder:text-slate-600 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 disabled:cursor-not-allowed disabled:opacity-60"
                />

                <button
                  type="submit"
                  disabled={isLoading}
                  className="rounded-2xl bg-blue-500 px-7 py-4 font-semibold transition hover:bg-blue-400 disabled:cursor-not-allowed disabled:bg-slate-700 disabled:text-slate-400"
                >
                  {isLoading
                    ? "Analyzing..."
                    : "Analyze repository"}
                </button>
              </form>
            </div>

            <div className="mx-auto mt-7 flex max-w-2xl items-center gap-4">
              <div className="h-px flex-1 bg-slate-800" />

              <span className="text-xs font-medium uppercase tracking-[0.2em] text-slate-600">
                Existing repositories
              </span>

              <div className="h-px flex-1 bg-slate-800" />
            </div>

            <button
              type="button"
              onClick={handleOpenRepositories}
              disabled={isLoadingRepositories}
              className="mx-auto mt-5 rounded-xl border border-slate-700 bg-slate-800 px-6 py-3 font-semibold text-slate-200 transition hover:border-blue-500/50 hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isLoadingRepositories
                ? "Loading repositories..."
                : showRepositories
                  ? "Refresh repositories"
                  : "Open repository"}
            </button>

            {showRepositories && (
              <div className="mx-auto mt-6 grid max-w-2xl gap-3 text-left sm:grid-cols-2">
                {repositories.length > 0 ? (
                  repositories.map((repo) => (
                    <button
                      key={repo.id}
                      type="button"
                      onClick={() =>
                        handleRepositorySelection(repo)
                      }
                      className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5 text-left transition hover:border-blue-500/50 hover:bg-slate-900"
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div className="min-w-0">
                          <p className="truncate font-semibold text-white">
                            {repo.owner}/{repo.name}
                          </p>

                          <p className="mt-1 truncate text-sm text-slate-500">
                            {repo.github_url}
                          </p>
                        </div>

                        <span className="shrink-0 rounded-full bg-slate-800 px-2.5 py-1 font-mono text-xs text-slate-400">
                          #{repo.id}
                        </span>
                      </div>

                      <div className="mt-4 flex items-center justify-between text-xs text-slate-500">
                        <span>
                          Branch: {repo.default_branch}
                        </span>

                        <span>
                          {repo.ingestion_status}
                        </span>
                      </div>
                    </button>
                  ))
                ) : (
                  <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5 text-center text-sm text-slate-500 sm:col-span-2">
                    No repositories have been ingested yet.
                  </div>
                )}
              </div>
            )}

            {repositoryError && (
              <div className="mx-auto mt-5 max-w-2xl rounded-2xl border border-red-400/20 bg-red-400/10 px-5 py-4 text-left text-sm text-red-300">
                {repositoryError}
              </div>
            )}
          </div>
        </section>

        {repository && (
          <section className="mx-auto w-full max-w-4xl pb-16">
            <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl backdrop-blur">
              <div className="flex flex-col gap-4 border-b border-slate-800 pb-5 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="h-2.5 w-2.5 rounded-full bg-emerald-400" />

                    <p className="text-sm font-medium text-emerald-400">
                      Repository ready
                    </p>
                  </div>

                  <h2 className="mt-2 text-2xl font-semibold">
                    {repository.owner}/{repository.name}
                  </h2>

                  <p className="mt-1 text-sm text-slate-500">
                    Branch: {repository.default_branch}
                  </p>
                </div>

                <span className="w-fit rounded-full border border-slate-700 bg-slate-950 px-3 py-1.5 font-mono text-xs text-slate-400">
                  repository #{repository.id}
                </span>
              </div>

              <form
                onSubmit={handleQuestionSubmit}
                className="mt-6"
              >
                <label
                  htmlFor="repository-question"
                  className="mb-2 block text-sm font-medium text-slate-300"
                >
                  Ask a question
                </label>

                <textarea
                  id="repository-question"
                  value={question}
                  onChange={(event) =>
                    setQuestion(event.target.value)
                  }
                  placeholder="How does repository ingestion work?"
                  required
                  disabled={isAsking}
                  rows={4}
                  className="w-full resize-none rounded-2xl border border-slate-700 bg-slate-950 px-5 py-4 text-white outline-none transition placeholder:text-slate-600 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 disabled:cursor-not-allowed disabled:opacity-60"
                />

                <button
                  type="submit"
                  disabled={isAsking}
                  className="mt-3 w-full rounded-2xl bg-blue-500 px-6 py-4 font-semibold transition hover:bg-blue-400 disabled:cursor-not-allowed disabled:bg-slate-700 disabled:text-slate-400"
                >
                  {isAsking
                    ? "Searching the codebase..."
                    : "Ask about this repository"}
                </button>
              </form>
            </div>

            {questionError && (
              <div className="mt-5 rounded-2xl border border-red-400/20 bg-red-400/10 px-5 py-4 text-sm text-red-300">
                {questionError}
              </div>
            )}
          </section>
        )}

        <footer className="mt-auto border-t border-slate-800/70 py-8 text-center text-sm text-slate-600">
          Built with FastAPI, PostgreSQL, pgvector, and
          React
        </footer>
      </div>
    </main>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/results" element={<ResultsPage />} />
    </Routes>
  )
}

export default App