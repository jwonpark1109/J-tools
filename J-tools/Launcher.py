import os
import ctypes
import subprocess
from nbt import nbt

# 1. UI & Path Configuration
ctypes.windll.kernel32.SetConsoleTitleW("J Tool Launcher")

def show_error_dialog(title, message):
    """윈도우 메시지 박스로 에러 알림"""
    ctypes.windll.user32.MessageBoxW(0, str(message), str(title), 0x10)

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
J_TOOLS_ROOT = BASE_PATH
SLOT_FILE_PATH = os.path.join(J_TOOLS_ROOT, "data", "slot-data.dat")

# --- UI Functions ---
def show_help():
    print("\n" + "="*55)
    print("            J TOOL LAUNCHER COMMAND HELP")
    print("="*55)
    print("  help                    : Show this help menu")
    print("  tool /list              : List all tools in 'tools/'")
    print("  tool /start {id}        : Run a tool by its ID")
    print("  files /tree             : Display directory structure")
    print("  files /tree /nbt        : Display files + full NBT tags")
    print("  files /tree /data       : Display files + 'data:' IDs")
    print("  slot /add {num} {id}    : Register tool to slot:num (1-9)")
    print("  slot /list              : View all registered slot:N commands")
    print("  slot:{num}              : Run tool registered in that slot")
    print("  exit / quit             : Terminate the launcher")
    print("="*55)

# --- NBT & Slot Logic ---
def get_slot_map():
    slot_map = {}
    if not os.path.exists(SLOT_FILE_PATH): return slot_map
    try:
        n_file = nbt.NBTFile(SLOT_FILE_PATH, 'rb')
        slots = n_file["main"]["data0"]["slots"]
        for entry in slots:
            key_cmd = str(entry.get("key", ""))
            tool_id = ""
            if "start" in entry:
                tool_id = str(entry["start"].get("tool_name", ""))
            if key_cmd and tool_id:
                slot_map[key_cmd] = tool_id
    except: pass
    return slot_map

# --- Core Management ---
def load_tool_registry():
    registry = {}
    tools_dir = os.path.join(J_TOOLS_ROOT, "tools")
    if not os.path.exists(tools_dir): return registry
    for root, dirs, files in os.walk(tools_dir):
        if "tool-data.dat" in files:
            try:
                n_file = nbt.NBTFile(os.path.join(root, "tool-data.dat"), 'rb')
                # 재귀적으로 tool id 찾기
                def find_tid(tag):
                    if isinstance(tag, nbt.TAG_Compound):
                        if "tool id" in tag: return str(tag["tool id"])
                        for k in tag:
                            res = find_tid(tag[k])
                            if res: return res
                    return None
                tid = find_tid(n_file)
                if tid: registry[tid] = {"folder": root}
            except: continue
    return registry

def run_tool(tool_id, registry):
    if tool_id in registry:
        info = registry[tool_id]
        bat_path = os.path.join(info['folder'], "tool.bat")
        if os.path.exists(bat_path):
            print(f"🚀 Executing {tool_id}...")
            subprocess.run([bat_path], shell=True, cwd=info['folder'])
        else: show_error_dialog("Missing File", f"tool.bat not found in:\n{info['folder']}")
    else: show_error_dialog("Unknown ID", f"Tool ID '{tool_id}' not found.")

# 4. Main Loop
if __name__ == "__main__":
    print("--- J Tool Launcher v2.6 ---")
    print("Type 'help' to see the list of available commands.")
    
    while True:
        try:
            user_input = input("\nJ-tools > ").strip()
            if not user_input: continue
            parts = user_input.split()
            cmd_main = parts[0].lower()

            # 1. Help & Exit
            if cmd_main == "help":
                show_help()
            elif cmd_main in ["exit", "quit"]:
                break

            # 2. Tool Commands
            elif cmd_main == "tool":
                if "/list" in parts:
                    reg = load_tool_registry()
                    print(f"\n📦 Tools Found: {len(reg)}")
                    for tid in reg: print(f"  - {tid}")
                elif "/start" in parts and len(parts) >= 3:
                    run_tool(parts[2], load_tool_registry())

            # 3. Slot Commands
            elif cmd_main == "slot":
                if "/add" in parts and len(parts) >= 4:
                    num = parts[2]
                    target_tid = parts[3]
                    if not num.isdigit():
                        show_error_dialog("Input Error", "Slot number must be a digit (e.g., 1).")
                        continue
                    
                    slot_key = f"slot:{num}"
                    try:
                        os.makedirs(os.path.dirname(SLOT_FILE_PATH), exist_ok=True)
                        n_file = nbt.NBTFile(SLOT_FILE_PATH, 'rb') if os.path.exists(SLOT_FILE_PATH) else nbt.NBTFile()
                        if not n_file.name:
                            n_file.name = "root"
                            n_file["main"] = nbt.TAG_Compound(); n_file["main"]["data0"] = nbt.TAG_Compound()
                            n_file["main"]["data0"]["slots"] = nbt.TAG_List(type=nbt.TAG_Compound)
                        
                        slots_list = n_file["main"]["data0"]["slots"]
                        
                        # 중복된 슬롯 번호가 있는지 확인 후 업데이트 또는 추가
                        updated = False
                        for s in slots_list:
                            if str(s["key"]) == slot_key:
                                s["start"]["tool_name"] = nbt.TAG_String(target_tid)
                                updated = True
                                break
                        
                        if not updated:
                            if len(slots_list) < 9:
                                new_s = nbt.TAG_Compound()
                                new_s["key"] = nbt.TAG_String(slot_key)
                                new_s["start"] = nbt.TAG_Compound()
                                new_s["start"]["tool_name"] = nbt.TAG_String(target_tid)
                                slots_list.append(new_s)
                            else:
                                show_error_dialog("Limit", "Max 9 slots allowed.")
                                continue
                        
                        n_file.write_file(SLOT_FILE_PATH)
                        print(f"✅ Slot updated: {slot_key} -> {target_tid}")
                    except Exception as e: show_error_dialog("Error", e)
                
                elif "/list" in parts:
                    s_map = get_slot_map()
                    print(f"\n📂 Active Slots: {len(s_map)}/9")
                    for k in sorted(s_map.keys()): print(f"  [{k}] -> {s_map[k]}")

            # 4. Files Commands
            elif cmd_main == "files" and "/tree" in parts:
                from main_logic import display_tree # (기존 display_tree 로직 연결)
                if "/nbt" in parts:
                    display_tree(J_TOOLS_ROOT, show_nbt=True)
                elif "/data" in parts:
                    display_tree(os.path.join(J_TOOLS_ROOT, "data"), show_data_id=True)
                else: display_tree(J_TOOLS_ROOT)

            # 5. Slot Execution (slot:1, slot:2...)
            else:
                s_map = get_slot_map()
                if user_input in s_map:
                    run_tool(s_map[user_input], load_tool_registry())
                else:
                    print("❌ Invalid command. Type 'help' for list.")
                
        except Exception as e:
            show_error_dialog("Critical Error", e)
