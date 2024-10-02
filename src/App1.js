import logo from './logo.svg';
import './App.css';

function App() {
  let display = 'off';
  //const pStyle = { 
  //  backgroundColor: 'yellow',
  //  color: 'green'
  //}

  return (
    <div className="App">
      { display === 'on' ? (
        <div>
          <h1>아메리카노</h1>
          <p className='pStyle'>3000원</p>
        </div>
      ) : (
        <div>
          <h1>아메리카노</h1>
          <p className='pStyle'>준비중</p>
        </div>
      )}
      
      {/* 버튼을 추가 */}
      <div>
        <button onClick={() => alert("버튼 클릭됨!")}>버튼</button>
      </div>
    </div>
  );
}

export default App;
