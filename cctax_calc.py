
#****************************************************************************************************
# File Start!
#***************************************************************************************************/

#*
 #
 #  Copyright (c) 2024-2025 by flechazo. All rights reserved.
 #
 # Author : CarlChai LinFeng Chai flechazo
 # Website: flechazo.mba
 #
 # Change Logs:
 # Date           Author       Notes
 # 2025-06-20     cc          the first version
 #
#/

#****************************************************************************************************
# Include
#***************************************************************************************************/

#****************************************************************************************************
# Define
#***************************************************************************************************/

#****************************************************************************************************
# Type Define
#***************************************************************************************************/

class cctax_calc:
    # init #
    def __init__(self,ratio_pension:float = 0.08,ratio_medical:float = 0.02,ratio_unemployment:float = 0.005,ratio_housing_fund:float = 0.12):
        # ratio #
        self.ratio = {}
        self.ratio_pension = ratio_pension
        self.ratio_medical = ratio_medical
        self.ratio_unemployment = ratio_unemployment
        self.ratio_housing_fund = ratio_housing_fund

    def calc_insurance(self,insurance_base):
        # 养老保险 8%
        pension = insurance_base * self.ratio_pension
        # 医疗保险 2%
        medical = insurance_base * self.ratio_medical
        # 失业保险 0.5%
        unemployment = insurance_base * self.ratio_unemployment
        # 公积金 12%
        housing_fund = insurance_base * self.ratio_housing_fund

        return pension, medical, unemployment, housing_fund

    def calc_tax(self, salary):
        # calculate tax
        if salary <= 3000:
            return salary * 0.03
        elif salary <= 12000:
            return salary * 0.1 - 210
        elif salary <= 25000:
            return salary * 0.2 - 1410
        elif salary <= 35000:
            return salary * 0.25 - 2660
        elif salary <= 55000:
            return salary * 0.3 - 4410
        elif salary <= 80000:
            return salary * 0.35 - 7160
        else:
            return salary * 0.45 - 15160

    def calc(self,salary,insurance_base):
        # calc steps #
        steps = []
        steps.append({'desc': '税前工资','value': salary})
        steps.append({'desc': '社保基数','value': insurance_base})
        # get insurance #
        pension, medical, unemployment, housing_fund = self.calc_insurance(insurance_base)
        steps.append({'desc': f'养老保险 ({self.ratio_pension * 100}%)', 'formula': f'{insurance_base} * 0.08', 'value': pension})
        steps.append({'desc': f'医疗保险 ({self.ratio_medical * 100}%)', 'formula': f'{insurance_base} * 0.02', 'value': medical})
        steps.append({'desc': f'失业保险 ({self.ratio_unemployment * 100}%)', 'formula': f'{insurance_base} * 0.005', 'value': unemployment})
        steps.append({'desc': f'公积金 ({self.ratio_housing_fund * 100}%)', 'formula': f'{insurance_base} * 0.12', 'value': housing_fund})
        # total #
        total_insurance = pension + medical + unemployment + housing_fund
        steps.append({'desc': '社保及公积金合计', 'formula': f'{pension} + {medical} + {unemployment} + {housing_fund}', 'value': total_insurance})

        # tax #
        taxable_income = salary - total_insurance - 5000
        steps.append({'desc': '应纳税所得额', 'formula': f'{salary} - {total_insurance} - 5000', 'value': taxable_income})
        if taxable_income <= 0:
            tax = 0
            steps.append({'desc': '个人所得税', 'formula': '应纳税所得额 <= 0, 税=0', 'value': tax})
        else:
            tax = self.calc_tax(taxable_income)
            steps.append({'desc': '个人所得税', 'formula': '分级税率计算', 'value': tax})
        after_tax = salary - total_insurance - tax
        steps.append({'desc': '税后收入', 'formula': f'{salary} - {total_insurance} - {tax}', 'value': after_tax})

        # detail #
        detail = f"税前工资: {salary:.2f}\n社保基数: {insurance_base:.2f}\n"
        detail += f"养老保险 (8%): {pension:.2f}\n"
        detail += f"医疗保险 (2%): {medical:.2f}\n"
        detail += f"失业保险 (0.5%): {unemployment:.2f}\n"
        detail += f"公积金 (12%): {housing_fund:.2f}\n"
        detail += f"社保及公积金合计: {total_insurance:.2f}\n"
        detail += f"应纳税所得额 = 税前工资 - 社保及公积金 - 起征点(5000): {taxable_income:.2f}\n"
        if taxable_income <= 0:
            detail += "应纳税所得额不大于0，无需缴税。\n"
        else:
            detail += f"个人所得税: {tax:.2f}\n"
        detail += f"税后收入 = 税前工资 - 社保及公积金 - 个人所得税: {after_tax:.2f}\n"
        
        # result #
        result = (
            f"{salary:.2f}",
            f"{insurance_base:.2f}",
            f"{pension:.2f}",
            f"{medical:.2f}",
            f"{unemployment:.2f}",
            f"{housing_fund:.2f}",
            f"{taxable_income:.2f}",
            f"{tax:.2f}",
            f"{after_tax:.2f}"
        )

        return result,detail,steps

#****************************************************************************************************
# Global Variable
#***************************************************************************************************/

#****************************************************************************************************
# Function Impletement
#***************************************************************************************************/

#****************************************************************************************************
# exports
#***************************************************************************************************/

#****************************************************************************************************
# File End!
#***************************************************************************************************/
