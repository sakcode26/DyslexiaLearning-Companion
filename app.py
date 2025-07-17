import React from "react";

const App = () => {
  return (
    <div className="min-h-screen bg-gradient-to-r from-purple-700 to-blue-500 flex flex-col items-center justify-center text-white">
      <h1 className="text-5xl font-bold mb-10 text-center">Autism cum Dyslexia Learning Companion</h1>
      <div className="flex flex-col gap-6 items-center">
        <button className="w-80 h-24 text-2xl font-semibold bg-green-500 hover:bg-green-600 transition-all rounded-xl shadow-lg">Autism Support System</button>
        <button className="w-80 h-24 text-2xl font-semibold bg-blue-500 hover:bg-blue-600 transition-all rounded-xl shadow-lg">Dyslexia Support System</button>
      </div>
    </div>
  );
};

export default App;
