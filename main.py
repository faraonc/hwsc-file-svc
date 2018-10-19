import service.hwsc_file_svc as hwsc_file_svc

if __name__ == '__main__':
    hwsc_file_svc.FileService().start(50051)