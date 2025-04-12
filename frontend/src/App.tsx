import AppRoutes from "./routes"


function App() {
  return (
    <div>
      <AppRoutes />
      <h1>This is test page.</h1>
      <li>
        <ol>
          <a href="/purchase"> Purchase </a>
        </ol>
        <ol>
          <a href="/restore"> Restore </a>
        </ol>
      </li>
    </div>

  )
}

export default App
