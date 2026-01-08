import { useState } from 'react';
import axios from 'axios';
import { BookOpen, BrainCircuit, Loader2 } from 'lucide-react';
import './App.css'; // 保持默认样式引用

function App() {
  const [topic, setTopic] = useState('');
  const [difficulty, setDifficulty] = useState('普通');
  const [loading, setLoading] = useState(false);
  const [questionData, setQuestionData] = useState(null);
  const [error, setError] = useState('');

  // 调用后端 API
  const handleGenerate = async () => {
    if (!topic) return;
    
    setLoading(true);
    setError('');
    setQuestionData(null);

    try {
      // 这里的地址要对应你后端的实际地址
      const response = await axios.post('http://127.0.0.1:8000/api/generate-quiz', {
        topic: topic,
        difficulty: difficulty
      });

      if (response.data.status === 'success') {
        setQuestionData(response.data.data);
      }
    } catch (err) {
      console.error(err);
      setError('生成失败，请检查后端服务是否启动。');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
      {/* 标题区 */}
      <header style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '2rem' }}>
        <BookOpen size={32} color="#646cff" />
        <h1>高中历史出题 Agent</h1>
      </header>

      {/* 输入区 */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '2rem' }}>
        <input
          type="text"
          placeholder="输入历史考点 (如: 洋务运动、辛亥革命)"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          style={{ flex: 1, padding: '10px', fontSize: '1rem' }}
        />
        
        <select 
          value={difficulty} 
          onChange={(e) => setDifficulty(e.target.value)}
          style={{ padding: '10px', fontSize: '1rem' }}
        >
          <option value="简单">简单</option>
          <option value="普通">普通</option>
          <option value="困难">困难</option>
        </select>

        <button 
          onClick={handleGenerate} 
          disabled={loading || !topic}
          style={{ padding: '10px 20px', fontSize: '1rem', cursor: 'pointer' }}
        >
          {loading ? <Loader2 className="spin" /> : <><BrainCircuit size={18} /> 生成题目</>}
        </button>
      </div>

      {/* 错误提示 */}
      {error && <div style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>}

      {/* 题目展示卡片 */}
      {questionData && (
        <div style={{ 
          border: '1px solid #ddd', 
          borderRadius: '8px', 
          padding: '2rem',
          backgroundColor: '#f9f9f9',
          textAlign: 'left' 
        }}>
          <h2 style={{ marginTop: 0 }}>题目预览</h2>
          <p style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>{questionData.question_text}</p>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', margin: '1.5rem 0' }}>
            {questionData.options.map((opt, index) => (
              <div key={index} style={{ 
                padding: '10px', 
                background: 'white', 
                border: '1px solid #ccc', 
                borderRadius: '4px' 
              }}>
                {opt}
              </div>
            ))}
          </div>
          <div style={{ marginTop: '2rem', paddingTop: '1.5rem', borderTop: '1px solid #eee' }}>
            {/* 答案行 */}
            <div style={{ marginBottom: '1rem', fontSize: '1.1rem', color: '#2c3e50', display: 'flex', alignItems: 'center' }}>
              <strong>✅ 正确答案：</strong>
              <span style={{ 
                color: '#fff', 
                backgroundColor: '#28a745', 
                padding: '2px 10px', 
                borderRadius: '4px', 
                marginLeft: '10px',
                fontSize: '1rem'
              }}>
                {questionData.correct_answer}
              </span>
            </div>

            {/* 专家解析卡片 */}
            <div style={{
              backgroundColor: '#f8f9fa',
              borderRadius: '8px',
              borderLeft: '5px solid #007bff', // 那个专业的蓝条
              padding: '1.5rem',
              marginTop: '10px',
              boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
            }}>
              <div style={{ marginBottom: '12px', display: 'flex', alignItems: 'center' }}>
                <span style={{
                  backgroundColor: '#e7f1ff',
                  color: '#0056b3',
                  fontSize: '13px',
                  padding: '4px 12px',
                  borderRadius: '20px',
                  fontWeight: 'bold',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '5px'
                }}>
                  <BrainCircuit size={14} /> 专家解析
                </span>
              </div>
              
              <div style={{ 
                whiteSpace: 'pre-wrap', // 保持后端返回的换行格式
                lineHeight: '1.8', 
                color: '#4a5568',
                fontSize: '15px',
                textAlign: 'justify'
              }}>
                {questionData.explanation}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;