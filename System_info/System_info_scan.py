import psutil
import GPUtil
import platform
import subprocess

def os_info():
    def get_current_user():
        users_info = psutil.users()
        return users_info[0].name
    

    print("="*40, "OS Information", "="*40)
    print(f"Current user: {get_current_user()}")
    print(f"System: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Version: {platform.version()}")
    print(f"Machine: {platform.machine()}")

def motherboard_info():
    def get_model():
        result = subprocess.run(["wmic", "baseboard", "get", "product"], capture_output=True, text=True)
        lines = result.stdout.split("\n")
        lines = [line.strip() for line in lines if line.strip()]
        if len(lines) > 1:
            return lines[1].replace("  ", " ")
        else:
            return "Unknown Motherboard"

    def get_manufacturer():
        result = subprocess.run(["wmic", "baseboard", "get", "manufacturer"], capture_output=True, text=True)
        lines = result.stdout.split("\n")
        lines = [line.strip() for line in lines if line.strip()]
        if len(lines) > 1:
            return lines[1].replace("  ", " ")
        else:
            return "Unknown Manufacturer"

    def get_serial_number():
        result = subprocess.run(["wmic", "baseboard", "get", "serialnumber"], capture_output=True, text=True)
        lines = result.stdout.split("\n")
        lines = [line.strip() for line in lines if line.strip()]
        if len(lines) > 1:
            return lines[1].replace("  ", " ")
        else:
            return "Unknown Serial Number"

    def get_version():
        try:
            result = subprocess.run(["wmic", "bios", "get","version"], capture_output=True, text=True)
            lines = result.stdout.split("\n")
            lines = [line.strip() for line in lines if line.strip()]
            if len(lines) > 1:
                return lines[1:]
            else:
                return "Unknown Verison"
        except Exception as e:
            return [str(e)]
    
    def get_system_type():
        result = subprocess.run(["powershell", "-Command", "($env:firmware_type)"], capture_output=True, text=True)
        return result.stdout

    print("="*40, "Motherboard Information", "="*40)
    print(f"Model: {get_model()}")
    print(f"Version: {get_version()}")
    print(f"Serial Number: {get_serial_number()}")
    print(f"Manufacturer: {get_manufacturer()}")
    print(f"UEFI/BIOS:  {get_system_type()}")

def cpu_info():
    def get_processor_name():
        result = subprocess.run(["wmic", "cpu", "get", "name"], capture_output=True, text=True).stdout
        lines = result.split("\n")
        lines = [line.strip() for line in lines if line.strip()]
        if len(lines) > 1:
            return lines[1].replace("  ", " ")
        else:
            return "Unknown Processor Model"
        
    print("="*40, "CPU Information", "="*40)
    print(f"Processor: {get_processor_name()}")
    print(f"Model: {platform.processor()}")
    print(f"Architecture: {platform.architecture()}")
    print(f"CPU Logical Cores: {psutil.cpu_count(logical=True)}")
    print(f"CPU Physical Cores: {psutil.cpu_count(logical=False)}")

    
def gpu_info():
    print("="*40, "GPU Information", "="*40)
    gpu = GPUtil.getGPUs()
    print(f"Name: {gpu[0].name}")
    print(f"Temperature: {gpu[0].temperature}°C")
    print(f"Load: {gpu[0].load*100}%")
    print(f"Memory Total: {gpu[0].memoryTotal} MB")
    print(f"Memory Used: {gpu[0].memoryUsed} MB")
    print(f"Memory Free: {gpu[0].memoryFree} MB")
    print(f"Memory Utilization: {round(gpu[0].memoryUtil*100)}%")

def ram_info():
    print("="*40, "RAM Information", "="*40)
    print(f"Total Memory: {round(psutil.virtual_memory().total / (1024.0 ** 3), 2)} GB")
    print(f"Available Memory: {round(psutil.virtual_memory().available / (1024.0 ** 3), 2)} GB")
    print(f"Used Memory: {round(psutil.virtual_memory().used / (1024.0 ** 3), 2)} GB")
    print(f"Memory Used Percentage: {psutil.virtual_memory().percent}%")

def disk_info():
    print("="*40, "Disk Information", "="*40)
    result = subprocess.run(["wmic", "diskdrive", "get", "model"], capture_output=True, text=True)
    result_splited = result.stdout.split("\n")
    for result in result_splited:
        if len(result) > 1:
            print(result)
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"Mountpoint: {partition.mountpoint}")
        print(f"File System: {partition.fstype}")
        DSU = list(psutil.disk_usage(partition.mountpoint))
        print(f"Total Size: {round(DSU[0] / (1024.0 ** 3), 2)} GB")
        print(f"Used: {round(DSU[1] / (1024.0 ** 3), 2)} GB")
        print(f"Free: {round(DSU[2] / (1024.0 ** 3), 2)} GB")


if __name__ == "__main__":
    os_info()
    motherboard_info()
    cpu_info()
    gpu_info()
    ram_info()
    disk_info()

