import { useState } from "react"

function App() {
  const [githubUrl, setGithubUrl] = useState("")

  function handleSubmit(event: React.SubmitEvent<HTMLFormElement>) {
    event.preventDefault()

    console.log(githubUrl)
  }

  return (
    <main>
      <h1>AI Codebase Assistant</h1>

      <form onSubmit={handleSubmit}>
        <label htmlFor="github-url">GitHub repository URL</label>

        <input
          id="github-url"
          type="url"
          value={githubUrl}
          onChange={(event) => setGithubUrl(event.target.value)}
          placeholder="https://github.com/owner/repository"
          required
        />

        <button type="submit">Ingest repository</button>
      </form>
    </main>
  )
}

export default App