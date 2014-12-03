from wsgiref.simple_server import make_server
import psutil,datetime

def server_monitor(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'html; charset=utf-8')]
    start_response(status, headers)
    message = "<h1>Welcome to the Server Health monitor</h1>"
    message +="<table style=\"width:90%\"><table style=\"height:50%\">"
    #message += "<tr>"
    message +="<td style=\"background-color:yellow\"><strong>BOOT TIME:</strong></td>"
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    message +="<td style=\"background-color:yellow\">"+str(boot_time)   +"</t/t/td>"
    message +="</tr>"

    cpu_util = psutil.cpu_percent(interval=1, percpu=True)
    message += "<tr style=\"background-color:yellow\"><th rowspan=\"4\"><strong>CPU UTILIZATION</strong></th>"
    i=1
    
    for cpu in cpu_util:
        if cpu < 25:
             message += "<td style=\"background-color:green\">"
        else:
            message += "<td style=\"background-color:red\">"
            
        message += "CPU {} : {}%".format(i, cpu)
        
        i+=1
        message += "</td></tr>"
    
    mem = psutil.virtual_memory()
    message += "<tr>"
    message +="<td style=\"background-color:yellow\"><strong>AVAILABLE MEMORY:</strong></td>"
    message +="<td style=\"background-color:yellow\">"+str(mem.available)+"</td>"
    message +="</tr>"
    message += "<tr>"
    message +="<<td style=\"background-color:yellow\"><strong>USED MEMORY:</strong></td>"
    message +="<td style=\"background-color:yellow\">"+str(mem.used)+"</td>"
    message +="</tr>"
    message +="<td style=\"background-color:yellow\"><strong>USED PERCENTAGE:</strong></td>"
    message +="<td style=\"background-color:yellow\">"+str(mem.percent)+"</td>"
    message +="</tr>"

    return[bytes(message,'utf-8')]

httpd = make_server('', 8000,server_monitor)
print("Serving on port 8000...")


httpd.serve_forever()
