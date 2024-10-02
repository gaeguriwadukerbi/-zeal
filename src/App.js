import React from 'react';
import Menu from './components/Menu';
import Image from './components/Image';
import Content1 from './components/Contents';
import './App.css';


function App() {
    return (
        <div className="App">
            <Menu />
            <div className="Contents">
                <Image />
                <Content1 />
            </div>
        </div>
    );
}

export default App;
