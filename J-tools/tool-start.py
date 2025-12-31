import os
import ctypes
from nbt import nbt
import subprocess

# 콘솔 창 타이틀 설정
ctypes.windll.kernel32.SetConsoleTitleW("J Tool Launcher")

# 프로그램 파일이 있는 현재 폴더를 기준으로 설정
BASE_PATH = os.path.dirname(os.path.abspath(__file__)) 
TOOLS_DIR = os.path.join(BASE_PATH, "tools")

def load_tool_registry():
    """tools 폴더 내의 모든 tool-data.dat를 스캔"""
    registry = {}
    
    if not os.path.exists(TOOLS_DIR):
        return registry

    for root, dirs, files in os.walk(TOOLS_DIR):
        if "tool-data.dat" in files:
            file_path = os.path.join(root, "tool-data.dat")
            try:
                n_file = nbt.NBTFile(file_path, 'rb')
                # data-type의 id가 아닌 tool-data의 id를 추출
                tool_id = extract_tool_id(n_file)
                
                if tool_id:
                    registry[tool_id] = {
                        "folder": root,
                        "data_path": file_path
                    }
            except:
                continue
                
    return registry

def extract_tool_id(nbt_data):
    """
    이미지 구조 분석 기반: 
    main -> tool-data -> 'tool id' 태그를 우선적으로 탐색
    """
    try:
        # 1. 'main' 태그 접근
        if "main" in nbt_data:
            main_tag = nbt_data["main"]
            # 2. 'tool-data' 태그 접근
            if "tool-data" in main_tag:
                tool_data_tag = main_tag["tool-data"]
                # 3. 'tool id' 값 반환
                if "tool id" in tool_data_tag:
                    return str(tool_data_tag["tool id"])
    except:
        pass
    
    # 예외 상황을 위해 전체 재귀 탐색도 유지 (단, tool-data 계층 우선)
    def backup_search(tag):
        if isinstance(tag, nbt.TAG_Compound):
            if "tool id" in tag: return str(tag["tool id"])
            for sub in tag.values():
                res = backup_search(sub)
                if res: return res
        return None

    return backup_search(nbt_data)

def run_tool(tool_id, registry):
    """일치하는 툴의 폴더에서 tool.bat 실행"""
    if tool_id in registry:
        info = registry[tool_id]
        tool_folder = info['folder']
        bat_file = os.path.join(tool_folder, "tool.bat")
        
        if os.path.exists(bat_file):
            print(f"🚀 starting {tool_id}! Please wait...")
            try:
                subprocess.run([bat_file], shell=True, cwd=tool_folder)
            except Exception as e:
                print(f"❌ An error occurred while running: {e}")
        else:
            print(f"⚠️ Error: Not Found '{tool_folder}\\tool.bat' Sorry.")
    else:
        print(f"❌ '{tool_id}' does not exist. Please check your command.")

if __name__ == "__main__":
    print("--- J Tool Launcher v1.6 ---")
    print("by J Tools 2025 | build 251231")
    print("💡 Tip: Type 'tool /list' to see tools, or 'tool /start {id}' to run.")
    
    tool_list = load_tool_registry()

    while True:
        user_input = input("\nJ-tools > ").strip()

        if not user_input:
            continue

        parts = user_input.split()

        if user_input == "tool /list":
            if tool_list:
                print("\n📦 [Tool list]")
                for idx, t_id in enumerate(tool_list.keys(), 1):
                    print(f"  {idx}. {t_id}")
            else:
                print("💡 No Found Tool. Sorry!")
        
        elif len(parts) >= 3 and parts[0] == "tool" and parts[1] == "/start":
            target_id = parts[2]
            run_tool(target_id, tool_list)

        elif user_input in ["exit", "quit"]:
            break
            
        else:
            print("❌ Unknown command. Use 'tool /list' or 'tool /start {id}'.")

