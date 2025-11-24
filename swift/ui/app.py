# Copyright (c) Alibaba, Inc. and its affiliates.
import os
from functools import partial
from typing import List, Optional, Union

import gradio as gr
from packaging import version
from transformers.utils import strtobool


def get_custom_css():
    """Return custom CSS from the style.css file"""
    css_path = os.path.join(os.path.dirname(__file__), 'style.css')
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

import swift
from swift.llm import (DeployArguments, EvalArguments, ExportArguments, RLHFArguments, SamplingArguments, SwiftPipeline,
                       WebUIArguments)
from swift.ui.llm_eval.llm_eval import LLMEval
from swift.ui.llm_export.llm_export import LLMExport
from swift.ui.llm_grpo.llm_grpo import LLMGRPO
from swift.ui.llm_infer.llm_infer import LLMInfer
from swift.ui.llm_rlhf.llm_rlhf import LLMRLHF
from swift.ui.llm_sample.llm_sample import LLMSample
from swift.ui.llm_train.llm_train import LLMTrain

locale_dict = {
    'title': {
        'zh': '轻量级大模型训练推理平台',
        'en': 'Lightweight Large Model Training and Inference Platform'
    },
    'sub_title': {
        'zh': '',
        'en': '',
    },
    'star_beggar': {
        'zh':
        '喜欢<a href=\"https://github.com/modelscope/ms-swift\" target=\"_blank\">SWIFT</a>就动动手指给我们加个star吧🥺 ',
        'en':
        'If you like <a href=\"https://github.com/modelscope/ms-swift\" target=\"_blank\">SWIFT</a>, '
        'please take a few seconds to star us🥺 '
    },
}


class SwiftWebUI(SwiftPipeline):

    args_class = WebUIArguments
    args: args_class

    def run(self):
        lang = os.environ.get('SWIFT_UI_LANG') or self.args.lang
        share_env = os.environ.get('WEBUI_SHARE')
        share = strtobool(share_env) if share_env else self.args.share
        server = os.environ.get('WEBUI_SERVER') or self.args.server_name
        port_env = os.environ.get('WEBUI_PORT')
        port = int(port_env) if port_env else self.args.server_port
        LLMTrain.set_lang(lang)
        LLMRLHF.set_lang(lang)
        LLMGRPO.set_lang(lang)
        LLMInfer.set_lang(lang)
        LLMExport.set_lang(lang)
        LLMEval.set_lang(lang)
        LLMSample.set_lang(lang)
        with gr.Blocks(title='SWIFT WebUI', theme=gr.themes.Base(), css=get_custom_css()) as app:
            try:
                _version = swift.__version__
            except AttributeError:
                _version = ''
            logo_svg = ''
            try:
                logo_path = os.path.join(os.path.dirname(__file__), 'images', 'logo.svg')
                with open(logo_path, 'r', encoding='utf-8') as _f:
                    logo_svg = _f.read()
            except Exception:
                logo_svg = '<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg"><line x1="8" y1="8" x2="32" y2="32" /><line x1="32" y1="8" x2="8" y2="32" /></svg>'
            
            with gr.Row():
                # 左侧导航栏
                with gr.Column(scale=1, min_width=350, elem_classes="sidebar"):
                    gr.HTML(f"""
                    <div class="sidebar-logo">
                        {logo_svg}
                    </div>
                    <div class="sidebar-header">新大陆大模型训练推理平台</div>
                    <div class="sidebar-menu">
                        <div class="sidebar-menu-item active" id="group-train">
                            <svg width="20" height="19" viewBox="0 0 20 19" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M16.285 3.54822C14.93 3.54822 13.82 4.61697 13.82 5.92322C13.82 6.16072 13.82 6.27947 13.9437 6.51697L10 8.65447L6.05625 6.51697C6.18 6.27947 6.18 6.16072 6.18 5.92322C6.18 4.61697 5.07 3.54822 3.715 3.54822C2.35875 3.54822 1.25 4.61697 1.25 5.92322C1.25 7.22947 2.35875 8.29822 3.715 8.29822C4.45375 8.29822 5.07 7.94197 5.56375 7.46697L9.38375 9.60447L9.38375 13.7607C8.275 13.9982 7.535 14.9482 7.535 16.0169C7.535 17.3232 8.64375 18.3919 10 18.3919C11.3562 18.3919 12.465 17.3232 12.465 16.0169C12.465 14.9482 11.725 13.9982 10.6162 13.7607L10.6162 9.60447L14.56 7.58572C14.93 7.94197 15.5462 8.29822 16.285 8.29822C17.6412 8.29822 18.75 7.22947 18.75 5.92322C18.75 4.61697 17.6412 3.54822 16.285 3.54822ZM3.715 7.11072C2.975 7.11072 2.4825 6.63572 2.4825 5.92322C2.4825 5.21072 2.975 4.73572 3.715 4.73572C4.45375 4.73572 4.9475 5.21072 4.9475 5.92322C4.9475 6.63572 4.45375 7.11072 3.715 7.11072ZM11.2325 16.0169C11.2325 16.7295 10.6162 17.2045 10 17.2045C9.26 17.2045 8.7675 16.7295 8.7675 16.0169C8.7675 15.3045 9.26 14.8295 10 14.8295C10.74 14.8295 11.2325 15.3045 11.2325 16.0169ZM16.285 7.11072C15.5462 7.11072 15.0525 6.63572 15.0525 5.92322C15.0525 5.21072 15.5462 4.73572 16.285 4.73572C17.0237 4.73572 17.5175 5.21072 17.5175 5.92322C17.5175 6.63572 17.0237 7.11072 16.285 7.11072Z" fill="#275EF4"/>
                            </svg>
                            <span>模型训练</span>
                        </div>
                        <!-- 模型训练子菜单 -->
                        <div id="train-submenu" class="submenu" style="display: block !important; margin-left: 20px; margin-top: 10px;">
                            <div class="sidebar-menu-item inactive" data-tab="llm_train">
                                <span>LLM预训练/微调</span>
                            </div>
                            <div class="sidebar-menu-item inactive" data-tab="llm_rlhf">
                                <span>LLM人类对齐</span>
                            </div>
                            <div class="sidebar-menu-item inactive" data-tab="llm_grpo">
                                <span>LLM GRPO</span>
                            </div>
                        </div>
                        <div class="sidebar-menu-item inactive" id="group-infer">
                            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M11.1478 0.64307L17.9509 4.44076C18.2227 4.59241 18.3893 4.88106 18.3847 5.1923L18.3847 14.0869C18.3846 14.9175 17.9231 15.6792 17.187 16.0638L11.0332 19.2792C10.386 19.6174 9.61422 19.6174 8.96702 19.2792L2.81317 16.0638C2.07705 15.6792 1.61556 14.9175 1.61548 14.0869L1.61548 5.1923C1.61585 4.8872 1.78044 4.60592 2.04625 4.45615L8.81548 0.646917C9.5392 0.239592 10.4227 0.238135 11.1478 0.64307ZM3.00009 11.1561L3.00009 14.0869C3.00009 14.4023 3.17548 14.6908 3.45394 14.8369L9.40471 17.9461L9.40471 14.5515L3.00009 11.1561ZM17 11.3946L10.6355 14.6561L10.6355 17.9246L16.5455 14.8369C16.8249 14.6911 17 14.4021 17 14.0869L17 11.3946ZM17 6.18845L11.0632 9.53461C10.9279 9.61085 10.7847 9.67223 10.6362 9.71769L10.6355 13.2738L17 10.0123L17 6.18922L17 6.18845ZM3.00009 6.19999L3.00009 9.76153L9.40471 13.1577L9.40471 9.72615C9.24932 9.67999 9.09702 9.61769 8.9524 9.53615L3.00009 6.20076L3.00009 6.19999Z" fill="#11193C"/>
                            </svg>
                            <span>模型服务</span>
                        </div>
                        <!-- 模型服务子菜单 -->
                        <div id="infer-submenu" class="submenu" style="display: block !important; margin-left: 20px; margin-top: 10px;">
                            <div class="sidebar-menu-item inactive" data-tab="llm_infer">
                                <span>LLM推理</span>
                            </div>
                            <div class="sidebar-menu-item inactive" data-tab="llm_export">
                                <span>LLM导出</span>
                            </div>
                        </div>
                        <div class="sidebar-menu-item inactive" id="group-eval">
                            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M18.16 1.75C18.21 1.75 18.25 1.79 18.25 1.84L18.25 15.56C18.25 15.61 18.21 15.65 18.16 15.65L1.84 15.65C1.79 15.65 1.75 15.61 1.75 15.56L1.75 1.84C1.75 1.79 1.79 1.75 1.84 1.75L18.16 1.75ZM18.16 0L1.84 0C0.82 0 0 0.82 0 1.84L0 15.56C0 16.58 0.82 17.4 1.84 17.4L18.16 17.4C19.18 17.4 20 16.58 20 15.56L20 1.84C20 0.82 19.18 0 18.16 0ZM15.6 19.125C15.6 18.64 15.21 18.25 14.72 18.25L5.27 18.25C4.79 18.25 4.4 18.64 4.4 19.125C4.4 19.61 4.79 20 5.27 20L14.72 20C15.21 20 15.6 19.61 15.6 19.125ZM8.6 6.125L13 8.7L8.57 11.25L8.57 6.145M8.19 4.11C7.44 4.12 6.83 4.74 6.84 5.5L6.84 11.92C6.84 12.68 7.46 13.29 8.21 13.28C8.45 13.29 8.69 13.22 8.89 13.1L14.47 9.88C15.38 9.36 15.38 8.04 14.47 7.51L8.89 4.3C8.69 4.18 8.45 4.11 8.21 4.11L8.19 4.11Z" fill="#11193C"/>
                            </svg>
                            <span>评测与演示</span>
                        </div>
                        <!-- 评测与演示子菜单 -->
                        <div id="eval-submenu" class="submenu" style="display: block !important; margin-left: 20px; margin-top: 10px;">
                            <div class="sidebar-menu-item inactive" data-tab="llm_eval">
                                <span>LLM评测</span>
                            </div>
                            <div class="sidebar-menu-item inactive" data-tab="llm_sample">
                                <span>LLM采样</span>
                            </div>
                        </div>
                    </div>
                    """, elem_classes="no-frame")
                
                # 右侧主内容区
                with gr.Column(scale=4, min_width=600, elem_classes="main-content"):
                    gr.HTML(f"<div class='top-title'>{locale_dict['title'][lang]}</div>", elem_classes="no-frame")
                    gr.HTML("<div id='page-tag' class='page-tag'></div>", elem_classes="no-frame")
                    with gr.Tabs():
                        LLMTrain.build_ui(LLMTrain)
                        LLMRLHF.build_ui(LLMRLHF)
                        LLMGRPO.build_ui(LLMGRPO)
                        LLMInfer.build_ui(LLMInfer)
                        LLMExport.build_ui(LLMExport)
                        LLMEval.build_ui(LLMEval)
                        LLMSample.build_ui(LLMSample)
            
            # 添加JavaScript代码实现菜单联动
            def js_script():
                return """
                function () {
                    function clickTabImpl(tabId) {
                        var tab = document.querySelector("button[aria-controls*='" + tabId + "']") ||
                                  document.querySelector("button[data-testid*='" + tabId + "']");
                        if (!tab) {
                            var allTabs = document.querySelectorAll('button');
                            for (var i = 0; i < allTabs.length; i++) {
                                if (allTabs[i].ariaControls && allTabs[i].ariaControls.indexOf(tabId) !== -1) { tab = allTabs[i]; break; }
                                var dt = allTabs[i].getAttribute('data-testid');
                                if (dt && dt.indexOf(tabId) !== -1) { tab = allTabs[i]; break; }
                            }
                        }
                        if (!tab) {
                            var selectors = ["[id*='" + tabId + "']", "[data-testid*='" + tabId + "']"]; 
                            for (var j = 0; j < selectors.length; j++) {
                                var el = document.querySelector(selectors[j]);
                                if (el) {
                                    var p = el.parentElement;
                                    while (p) {
                                        if (p.tagName === 'BUTTON' && p.classList.contains('tab-nav--item')) { p.click(); return; }
                                        p = p.parentElement;
                                    }
                                }
                            }
                        }
                        if (tab) { tab.click(); }
                    }
                    window.selectMenu = function(tabId, elem) {
                        clickTabImpl(tabId);
                        var subItems = document.querySelectorAll('.submenu .sidebar-menu-item');
                        for (var s = 0; s < subItems.length; s++) { subItems[s].classList.remove('active'); subItems[s].classList.add('inactive'); }
                        if (elem) { elem.classList.add('active'); elem.classList.remove('inactive'); }
                        var submenu = elem ? elem.closest('.submenu') : null;
                        var groups = document.querySelectorAll('.sidebar > .sidebar-menu > .sidebar-menu-item');
                        for (var g = 0; g < groups.length; g++) { groups[g].classList.remove('active'); groups[g].classList.add('inactive'); }
                        if (submenu && submenu.previousElementSibling && submenu.previousElementSibling.classList.contains('sidebar-menu-item')) {
                            submenu.previousElementSibling.classList.add('active');
                            submenu.previousElementSibling.classList.remove('inactive');
                        }
                        var tag = document.getElementById('page-tag');
                        if (tag) {
                            var text = '';
                            if (elem) {
                                var sp = elem.querySelector('span');
                                text = sp ? sp.innerText : elem.innerText;
                            }
                            tag.textContent = text;
                        }
                        var panel = document.getElementById(tabId);
                        if (panel) {
                            var container = panel.parentElement;
                            if (container) {
                                var allPanels = container.querySelectorAll('.tabitem');
                                for (var i = 0; i < allPanels.length; i++) { allPanels[i].style.display = 'none'; }
                            }
                            panel.style.display = 'block';
                        }
                    };
                    window.toggleSubmenu = function(submenuId, elem) {
                        var submenu = document.getElementById(submenuId);
                        if (!submenu) return;
                        submenu.style.display = 'block';
                        var groups2 = document.querySelectorAll('.sidebar-menu > .sidebar-menu-item');
                        for (var m = 0; m < groups2.length; m++) { groups2[m].classList.remove('active'); groups2[m].classList.add('inactive'); }
                        if (elem) { elem.classList.add('active'); elem.classList.remove('inactive'); }
                    };
                    document.addEventListener('click', function(e){
                        var btn = e.target.closest('button');
                        if (!btn) return;
                        var id = btn.getAttribute('aria-controls') || btn.getAttribute('data-testid');
                        if (!id) return;
                        var leaf = document.querySelector(".submenu .sidebar-menu-item[data-tab='" + id + "']");
                        if (leaf) { window.selectMenu(id, leaf); }
                    });
                    window.clickTab = clickTabImpl;
                    window.clickTabImpl = clickTabImpl;
                    var defaultLeaf = document.querySelector(".submenu .sidebar-menu-item[data-tab='llm_train']");
                    if (defaultLeaf) { window.selectMenu('llm_train', defaultLeaf); }
                    var menu = document.querySelector('.sidebar-menu');
                    if (menu) {
                        menu.addEventListener('click', function(e){
                            var leaf = e.target.closest('.sidebar-menu .submenu .sidebar-menu-item');
                            if (leaf && leaf.dataset && leaf.dataset.tab) { window.selectMenu(leaf.dataset.tab, leaf); return; }
                            var grpTrain = e.target.closest('#group-train');
                            if (grpTrain) { window.toggleSubmenu('train-submenu', grpTrain); return; }
                            var grpInfer = e.target.closest('#group-infer');
                            if (grpInfer) { window.toggleSubmenu('infer-submenu', grpInfer); return; }
                            var grpEval = e.target.closest('#group-eval');
                            if (grpEval) { window.toggleSubmenu('eval-submenu', grpEval); return; }
                        });
                    }
                    var wrapper = document.querySelector('.main-content .tab-wrapper');
                    var tag = document.getElementById('page-tag');
                    if (wrapper && tag) {
                        wrapper.insertBefore(tag, wrapper.firstChild);
                        var tabs = wrapper.querySelectorAll('.tab-container, .overflow-menu');
                        tabs.forEach(function(el){
                            el.style.visibility = 'hidden';
                            el.style.position = 'absolute';
                            el.style.left = '-9999px';
                            el.style.height = '0';
                            el.style.width = '0';
                            el.style.margin = '0';
                            el.style.padding = '0';
                        });
                    }
                    var footer = document.querySelector('footer');
                    if (footer) {
                        footer.innerHTML = '<div class="custom-footer">@福建新大陆软件工程有限公司</div>';
                    }
                }
                """
            
            app.load(None, None, None, js=js_script())

            concurrent = {}
            if version.parse(gr.__version__) < version.parse('4.0.0'):
                concurrent = {'concurrency_count': 5}
            
        app.queue(**concurrent).launch(server_name=server, inbrowser=True, server_port=port, height=800, share=share)


def webui_main(args: Optional[Union[List[str], WebUIArguments]] = None):
    return SwiftWebUI(args).main()
