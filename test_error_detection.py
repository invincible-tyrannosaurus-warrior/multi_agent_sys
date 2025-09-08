import subprocess
import sys
import os

# 模拟不同类型的错误输出
def test_should_use_glm_analysis():
    # 导入should_use_glm_analysis函数
    sys.path.append(os.path.dirname(__file__))
    from gpt4o_feedback_loop import should_use_glm_analysis
    
    # 测试用例1: 代码语法错误 - 应该使用GPT-4o
    stderr_syntax = "SyntaxError: invalid syntax"
    stdout_syntax = ""
    result1 = should_use_glm_analysis(stderr_syntax, stdout_syntax)
    print(f"语法错误测试: {result1} (应该是False)")
    
    # 测试用例2: 元素定位超时 - 应该使用GLM
    stderr_timeout = "TimeoutError: Waiting for selector 'text=Task Management' to be visible"
    stdout_timeout = ""
    result2 = should_use_glm_analysis(stderr_timeout, stdout_timeout)
    print(f"元素定位超时测试: {result2} (应该是True)")
    
    # 测试用例3: 导入错误 - 应该使用GPT-4o
    stderr_import = "ModuleNotFoundError: No module named 'playwright'"
    stdout_import = ""
    result3 = should_use_glm_analysis(stderr_import, stdout_import)
    print(f"导入错误测试: {result3} (应该是False)")
    
    # 测试用例4: 找不到元素 - 应该使用GLM
    stderr_element = "Error: Element not found: button:has-text('Task Management')"
    stdout_element = ""
    result4 = should_use_glm_analysis(stderr_element, stdout_element)
    print(f"元素未找到测试: {result4} (应该是True)")
    
    # 测试用例5: 空输出 - 应该使用GPT-4o（默认）
    stderr_empty = ""
    stdout_empty = ""
    result5 = should_use_glm_analysis(stderr_empty, stdout_empty)
    print(f"空输出测试: {result5} (应该是False)")

if __name__ == "__main__":
    test_should_use_glm_analysis()
