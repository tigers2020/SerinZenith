// theme/static_src/js/index.jsx
import React from 'react';
import ReactDOM from 'react-dom';
import { Input } from './components/input.jsx';  // 예시로 Input 컴포넌트를 사용합니다
import { Button } from './components/button.jsx';

function App() {
    return (
        <div>
            <h1>Welcome to Serin Zenith</h1>
            <form>
                <Input name="name" placeholder="Name" />
                <Button type="submit">Submit</Button>
            </form>
        </div>
    );
}

ReactDOM.render(<App />, document.getElementById('root'));
