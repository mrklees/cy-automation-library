import cyla_updater
import win32_wrapper

if __name__ == "__main__":
    win32_wrapper.configure_log('C:\\Users\\aperusse\\GitHub\\cy-automation-library\\cyautomation\\excel-updater')
    cyla_updater.update_all()