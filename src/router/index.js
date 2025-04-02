import Vue from 'vue';
import VueRouter from 'vue-router';

// todo public
import Login from "@/apps/LoginPage.vue";

// todo admin
import adminIndex from '@/apps/admin/LeftHome.vue';
// 用户部门管理
import adminUserDepartment from '@/apps/admin/UserDepartment.vue'
// 用户管理
import admin_user from '@/apps/admin/user/admin_user.vue'
import admin_auditor from '@/apps/admin/user/admin_auditor.vue'
import admin_finance from '@/apps/admin/user/admin_finance.vue'
import admin_admin from '@/apps/admin/user/admin_admin.vue'
// 供应商管理
import Supplier from '@/apps/admin/Supplier_view.vue'
// 材料信息管理
import Material from '@/apps/admin/Material_view.vue'
// 材料数量管理
import MaterialNumber from '@/apps/admin/Material_number_view.vue'
import Material_Hoistory_view from '@/apps/admin/Material_Hoistory_view.vue'


//todo user
import userIndex from '@/apps/user/LeftHome.vue';
// 计划内申请
import user_MonthlyPlan from '@/apps/user/MonthlyPlan.vue';
import user_MonthlyPlanHistory from '@/apps/user/MonthlyPlanHistory.vue';
// 计划外申请
import MonthlyPlanOuter from '@/apps/user/MonthlyPlanOuter.vue';
import MonthlyPlanOuterHistory from '@/apps/user/MonthlyPlanOuterHistory.vue';
import DayPlan from '@/apps/user/DayPlan.vue';
import DayPlanHistory from '@/apps/user/DayPlanHistory.vue';


//todo auditor
import auditorIndex from '@/apps/auditor/LeftHome.vue';
import auditor_MonthlyPlan from '@/apps/auditor/MonthlyPlan.vue';
import auditor_MonthlyPlanOuter from '@/apps/auditor/MonthlyPlanOuter.vue';
import auditor_DayPlan from '@/apps/auditor/DayPlan.vue';


//todo finance
import financeIndex from '@/apps/finance/LeftHome.vue';
import finance_MonthlyPlan from '@/apps/finance/MonthlyPlan.vue';
import finance_MonthlyPlanOuter from '@/apps/finance/MonthlyPlanOuter.vue';
import finance_DayPlan from '@/apps/finance/DayPlan.vue';
import excel_view from '@/apps/finance/excel_view.vue';
import excel_view_outer from '@/apps/finance/excel_view_outer.vue';
import table_view from '@/apps/finance/table_view.vue'


Vue.use(VueRouter);

const routes = [
    {
        path: '/login',
        component: Login,
    },
    {
        path: '/user',
        component: userIndex,
        children: [
            // todo 月计划申请
            {  //  月计划内 申请
                path: 'user_MonthlyPlan',
                component: user_MonthlyPlan
            },
            {   // 月计划内 历史记录
                path: 'user_MonthlyPlanHistory',
                component: user_MonthlyPlanHistory
            },
            {   // 月计划外 申请
                path: 'MonthlyPlanOuter',
                component: MonthlyPlanOuter
            },
            {   // 月计划外 历史记录
                path: 'MonthlyPlanOuterHistory',
                component: MonthlyPlanOuterHistory
            },
            {   // 日 申请
                path: 'DayPlan',
                component: DayPlan
            },
            {   // 日 历史记录
                path: 'DayPlanHistory',
                component: DayPlanHistory
            },

        ]
    },
    {
        path: '/auditor',
        component: auditorIndex,
        children: [
            {   // todo 月计划申请管理
                path: 'auditor_MonthlyPlan',
                component: auditor_MonthlyPlan
            },
            {   // todo 月计划外申请管理
                path: 'auditor_MonthlyPlanOuter',
                component: auditor_MonthlyPlanOuter
            },
            {   // todo 日计划外申请管理
                path: 'auditor_DayPlan',
                component: auditor_DayPlan
            },

        ]
    },
    {
        path: '/finance',
        component: financeIndex,
        children: [
            {   // todo 供应商管理
                path: 'Supplier',
                component: Supplier
            },
            {   // todo 月计划申请管理
                path: 'finance_MonthlyPlan',
                component: finance_MonthlyPlan
            },
            {   // todo 月计划外申请管理
                path: 'finance_MonthlyPlanOuter',
                component: finance_MonthlyPlanOuter
            },
            {   // todo 日计划外申请管理
                path: 'finance_DayPlan',
                component: finance_DayPlan
            },
            {   // todo 日计划外申请管理
                path: 'finance_DayPlan',
                component: finance_DayPlan
            },
            {   // todo 材料信息
                path: 'Material',
                component: Material
            },
            {   // todo 材料信息
                path: 'MaterialNumber',
                component: MaterialNumber
            },
            {   // todo excel_view
                path: 'excel_view',
                component: excel_view
            },
            {   // todo excel_view
                path: 'excel_view_outer',
                component: excel_view_outer
            },
            {   // todo excel_view
                path: 'table_view',
                component: table_view
            },
            {   // todo Material_Hoistory_view
                path: 'Material_Hoistory_view',
                component: Material_Hoistory_view
            },


        ]
    },
    {
        path: '/admin',
        component: adminIndex,
        children: [
            {   // todo 部门管理
                path: 'UserDepartment',
                component: adminUserDepartment
            },
            // todo 用户管理
            {   // 用户
                path: 'admin_user',
                component: admin_user
            },
            {   // 审核员
                path: 'admin_auditor',
                component: admin_auditor
            },
            {   // 财务
                path: 'admin_finance',
                component: admin_finance
            },
            {   // 管理员
                path: 'admin_admin',
                component: admin_admin
            },
            {   // todo 供应商管理
                path: 'Supplier',
                component: Supplier
            },
            {   // todo 材料信息
                path: 'Material',
                component: Material
            },
            {   // todo 材料信息
                path: 'MaterialNumber',
                component: MaterialNumber
            },


            {   // todo 月计划申请管理
                path: 'finance_MonthlyPlan',
                component: finance_MonthlyPlan
            },
            {   // todo 月计划外申请管理
                path: 'finance_MonthlyPlanOuter',
                component: finance_MonthlyPlanOuter
            },
            {   // todo 日计划外申请管理
                path: 'finance_DayPlan',
                component: finance_DayPlan
            },
            {   // todo 日计划外申请管理
                path: 'finance_DayPlan',
                component: finance_DayPlan
            },
            {   // todo excel_view
                path: 'excel_view',
                component: excel_view
            },
            {   // todo excel_view
                path: 'excel_view_outer',
                component: excel_view_outer
            },

            {   // todo Material_Hoistory_view
                path: 'Material_Hoistory_view',
                component: Material_Hoistory_view
            },


        ]
    },
];

const router = new VueRouter({
    mode: 'hash',
    routes
});

export default router;