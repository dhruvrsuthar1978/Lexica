import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './components/theme-provider';
import { Toaster } from './components/ui/sonner';
import { TooltipProvider } from './components/ui/tooltip';
import { Home } from './pages/Home';
import { Landing } from './pages/Landing';

function App() {
  return (
    <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
      <TooltipProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/app" element={<Home />} />
          </Routes>
        </BrowserRouter>
        <Toaster richColors position="top-right" />
      </TooltipProvider>
    </ThemeProvider>
  );
}

export default App;
