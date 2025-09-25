import React, { useState, useRef, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { aiToolService } from '../../services/api';
import './CodeEditor.css';

const CodeEditor = () => {
  const [code, setCode] = useState('// اكتب الكود هنا');
  const [language, setLanguage] = useState('javascript');
  const [theme, setTheme] = useState('vs-dark');
  const [isLoading, setIsLoading] = useState(false);
  const [aiResponse, setAiResponse] = useState(null);
  const [aiAction, setAiAction] = useState(null);
  const [prompt, setPrompt] = useState('');
  const [targetLanguage, setTargetLanguage] = useState('python');
  const editorRef = useRef(null);

  // قائمة اللغات المدعومة
  const supportedLanguages = [
    { id: 'javascript', name: 'JavaScript' },
    { id: 'typescript', name: 'TypeScript' },
    { id: 'python', name: 'Python' },
    { id: 'java', name: 'Java' },
    { id: 'csharp', name: 'C#' },
    { id: 'cpp', name: 'C++' },
    { id: 'php', name: 'PHP' },
    { id: 'ruby', name: 'Ruby' },
    { id: 'go', name: 'Go' },
    { id: 'rust', name: 'Rust' },
    { id: 'sql', name: 'SQL' },
    { id: 'html', name: 'HTML' },
    { id: 'css', name: 'CSS' },
    { id: 'json', name: 'JSON' },
    { id: 'markdown', name: 'Markdown' },
    { id: 'yaml', name: 'YAML' },
  ];

  // قائمة السمات المدعومة
  const supportedThemes = [
    { id: 'vs', name: 'فاتح' },
    { id: 'vs-dark', name: 'داكن' },
    { id: 'hc-black', name: 'تباين عالي (داكن)' },
    { id: 'hc-light', name: 'تباين عالي (فاتح)' },
  ];

  // تهيئة المحرر
  const handleEditorDidMount = (editor, monaco) => {
    editorRef.current = editor;
    
    // إضافة اقتراحات مخصصة
    monaco.languages.registerCompletionItemProvider('javascript', {
      provideCompletionItems: () => {
        return {
          suggestions: [
            {
              label: 'console.log',
              kind: monaco.languages.CompletionItemKind.Function,
              insertText: 'console.log($1);',
              insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
              detail: 'طباعة إلى وحدة التحكم',
            },
            {
              label: 'function',
              kind: monaco.languages.CompletionItemKind.Snippet,
              insertText: 'function ${1:name}(${2:params}) {\n\t$0\n}',
              insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
              detail: 'تعريف دالة',
            },
            {
              label: 'for',
              kind: monaco.languages.CompletionItemKind.Snippet,
              insertText: 'for (let ${1:i} = 0; ${1:i} < ${2:array}.length; ${1:i}++) {\n\t$0\n}',
              insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
              detail: 'حلقة for',
            },
          ],
        };
      },
    });
  };

  // استخدام أداة الذكاء الاصطناعي
  const useAITool = async (toolType) => {
    if (!editorRef.current) return;
    
    setIsLoading(true);
    setAiAction(toolType);
    setAiResponse(null);
    
    try {
      const currentCode = editorRef.current.getValue();
      
      let toolId;
      let requestData = {};
      
      switch (toolType) {
        case 'generate_code':
          toolId = 1; // افتراضي، يجب تحديثه بناءً على البيانات الفعلية
          requestData = {
            prompt: prompt,
            language: language
          };
          break;
          
        case 'debug_code':
          toolId = 2; // افتراضي، يجب تحديثه بناءً على البيانات الفعلية
          requestData = {
            prompt: prompt || 'تصحيح الأخطاء في الكود',
            code: currentCode,
            language: language
          };
          break;
          
        case 'explain_code':
          toolId = 3; // افتراضي، يجب تحديثه بناءً على البيانات الفعلية
          requestData = {
            prompt: 'شرح الكود',
            code: currentCode,
            language: language
          };
          break;
          
        case 'convert_code':
          toolId = 4; // افتراضي، يجب تحديثه بناءً على البيانات الفعلية
          requestData = {
            prompt: `تحويل الكود من ${language} إلى ${targetLanguage}`,
            code: currentCode,
            language: language,
            target_language: targetLanguage
          };
          break;
          
        default:
          throw new Error('نوع أداة غير معروف');
      }
      
      const response = await aiToolService.useAITool(toolId, requestData);
      setAiResponse(response);
      
      // تحديث المحرر بناءً على نوع الأداة
      if (toolType === 'generate_code' && response.generated_code) {
        setCode(response.generated_code);
      } else if (toolType === 'convert_code' && response.converted_code) {
        setCode(response.converted_code);
        setLanguage(targetLanguage);
      }
      
    } catch (error) {
      console.error('Error using AI tool:', error);
      setAiResponse({ error: 'حدث خطأ أثناء استخدام أداة الذكاء الاصطناعي' });
    } finally {
      setIsLoading(false);
    }
  };

  // تنفيذ الكود (محاكاة)
  const runCode = () => {
    const currentCode = editorRef.current.getValue();
    
    // محاكاة تنفيذ الكود (في الإنتاج، يمكن استخدام خدمة باك إند لتنفيذ الكود)
    try {
      // تنظيف وحدة التحكم
      console.clear();
      
      // إنشاء وظيفة console.log مخصصة لعرض النتائج
      const originalLog = console.log;
      const logs = [];
      
      console.log = (...args) => {
        logs.push(args.map(arg => 
          typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
        ).join(' '));
        originalLog(...args);
      };
      
      // تنفيذ الكود (ملاحظة: هذا يعمل فقط مع JavaScript وقد يكون غير آمن)
      if (language === 'javascript') {
        // eslint-disable-next-line no-new-func
        const executeCode = new Function(currentCode);
        executeCode();
      } else {
        logs.push(`تنفيذ الكود بلغة ${language} غير مدعوم في المتصفح. استخدم JavaScript للتنفيذ المباشر.`);
      }
      
      // استعادة وظيفة console.log الأصلية
      console.log = originalLog;
      
      // عرض النتائج
      setAiAction('run_code');
      setAiResponse({ output: logs.join('\n') });
      
    } catch (error) {
      setAiAction('run_code');
      setAiResponse({ error: `خطأ في التنفيذ: ${error.message}` });
    }
  };

  // حفظ الكود
  const saveCode = () => {
    const currentCode = editorRef.current.getValue();
    const blob = new Blob([currentCode], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `code.${language}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="code-editor-container">
      <div className="editor-toolbar">
        <div className="editor-settings">
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="language-selector"
          >
            {supportedLanguages.map((lang) => (
              <option key={lang.id} value={lang.id}>
                {lang.name}
              </option>
            ))}
          </select>
          
          <select
            value={theme}
            onChange={(e) => setTheme(e.target.value)}
            className="theme-selector"
          >
            {supportedThemes.map((theme) => (
              <option key={theme.id} value={theme.id}>
                {theme.name}
              </option>
            ))}
          </select>
        </div>
        
        <div className="editor-actions">
          <button onClick={runCode} className="run-button">
            <i className="fas fa-play"></i> تشغيل
          </button>
          <button onClick={saveCode} className="save-button">
            <i className="fas fa-save"></i> حفظ
          </button>
        </div>
      </div>
      
      <div className="editor-main">
        <div className="monaco-editor-wrapper">
          <Editor
            height="500px"
            language={language}
            theme={theme}
            value={code}
            onChange={(value) => setCode(value)}
            onMount={handleEditorDidMount}
            options={{
              minimap: { enabled: true },
              fontSize: 14,
              wordWrap: 'on',
              automaticLayout: true,
              tabSize: 2,
              scrollBeyondLastLine: false,
              renderLineHighlight: 'all',
              fontFamily: 'Fira Code, Consolas, monospace',
              fontLigatures: true,
              scrollbar: {
                verticalScrollbarSize: 10,
                horizontalScrollbarSize: 10,
              },
            }}
          />
        </div>
        
        <div className="ai-tools-panel">
          <h3>أدوات الذكاء الاصطناعي</h3>
          
          <div className="ai-tool-section">
            <h4>توليد الكود</h4>
            <div className="ai-tool-input">
              <input
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="اكتب وصفاً للكود الذي تريد إنشاءه..."
                className="ai-prompt-input"
              />
              <button
                onClick={() => useAITool('generate_code')}
                disabled={isLoading || !prompt}
                className="ai-tool-button"
              >
                {isLoading && aiAction === 'generate_code' ? 'جاري التوليد...' : 'توليد الكود'}
              </button>
            </div>
          </div>
          
          <div className="ai-tool-section">
            <h4>تصحيح الأخطاء</h4>
            <button
              onClick={() => useAITool('debug_code')}
              disabled={isLoading}
              className="ai-tool-button"
            >
              {isLoading && aiAction === 'debug_code' ? 'جاري التصحيح...' : 'تصحيح الأخطاء'}
            </button>
          </div>
          
          <div className="ai-tool-section">
            <h4>شرح الكود</h4>
            <button
              onClick={() => useAITool('explain_code')}
              disabled={isLoading}
              className="ai-tool-button"
            >
              {isLoading && aiAction === 'explain_code' ? 'جاري الشرح...' : 'شرح الكود'}
            </button>
          </div>
          
          <div className="ai-tool-section">
            <h4>تحويل الكود</h4>
            <div className="ai-tool-input">
              <select
                value={targetLanguage}
                onChange={(e) => setTargetLanguage(e.target.value)}
                className="language-selector"
              >
                {supportedLanguages
                  .filter((lang) => lang.id !== language)
                  .map((lang) => (
                    <option key={lang.id} value={lang.id}>
                      {lang.name}
                    </option>
                  ))}
              </select>
              <button
                onClick={() => useAITool('convert_code')}
                disabled={isLoading}
                className="ai-tool-button"
              >
                {isLoading && aiAction === 'convert_code' ? 'جاري التحويل...' : 'تحويل الكود'}
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {aiResponse && (
        <div className="ai-response">
          <h3>
            {aiAction === 'generate_code' && 'الكود المولد'}
            {aiAction === 'debug_code' && 'نتائج تصحيح الأخطاء'}
            {aiAction === 'explain_code' && 'شرح الكود'}
            {aiAction === 'convert_code' && 'الكود المحول'}
            {aiAction === 'run_code' && 'نتائج التنفيذ'}
          </h3>
          
          {aiResponse.error ? (
            <div className="ai-error">{aiResponse.error}</div>
          ) : (
            <div className="ai-result">
              {aiAction === 'generate_code' && (
                <pre>{aiResponse.generated_code}</pre>
              )}
              {aiAction === 'debug_code' && (
                <pre>{aiResponse.debug_result}</pre>
              )}
              {aiAction === 'explain_code' && (
                <div className="explanation">{aiResponse.explanation}</div>
              )}
              {aiAction === 'convert_code' && (
                <pre>{aiResponse.converted_code}</pre>
              )}
              {aiAction === 'run_code' && (
                <pre>{aiResponse.output}</pre>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CodeEditor;

