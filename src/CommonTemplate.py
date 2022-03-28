import time

from CommonLogger import LoggerServices as logger_services
from CommonOs import OsServices as os_services


class Template(os_services, logger_services):
    """This class contains the common input display method used across all scripts.

    The common display template is used for all scripts

    Args
        Required: none
        Optional: none

    Alerts: Critical | WARN | ERROR

    Logging: none
    """

    __author__ = "Barry Onizak"
    __version__ = "20220328.1"

    # # # # # End of header # # # #

    def display_template(self, parameter_list, args):
        """
        This method takes a list of cmd line args
        passed and displays each running script in a similar view
        """

        print(os_services.startScriptLine(self))

        print(f'{os_services.date()}: Extracting input Params:', *parameter_list)
        logger_services.info(self, f''"Extracting input params: {}".format(' '.join(map(str, parameter_list))))

        if hasattr(args, 'version'):
            print(f'{os_services.date()}: Script version : {args.version}')
            logger_services.info(self, f'Script version : {args.version}')
        else:
            print(f'{os_services.date()}: Script version : UNKNOWN')
            logger_services.info(self, f'Script version : UNKNOWN')

        if '-DSMC' in parameter_list:
            print(f'{os_services.date()}: Will DSMC query: {args.DSMC} for the last backup taken on DISK.')
        time.sleep(1)
        if '-MaxAge' in parameter_list:
            print(
                f'{os_services.date()}: MaxAge has been set to {args.MaxAge} (days), Will override default of 1 (day).')
        if '-parm' in parameter_list:
            print(
                f'{os_services.date()}: Additional Space Checking will be done using input file: {args.parm.name}..')

        return None
