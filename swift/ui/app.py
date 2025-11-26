# Copyright (c) Alibaba, Inc. and its affiliates.
import os
from functools import partial
from typing import List, Optional, Union

import gradio as gr
from packaging import version
from transformers.utils import strtobool

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
        'en': 'Scalable lightWeight Infrastructure for Fine-Tuning and Inference'
    },
    'sub_title': {
        'zh':
        '请查看 <a href=\"https://github.com/modelscope/ms-swift/tree/main/docs/source\" target=\"_blank\">'
        'SWIFT 文档</a>来查看更多功能，使用SWIFT_UI_LANG=en环境变量来切换英文界面',
        'en':
        'Please check <a href=\"https://github.com/modelscope/ms-swift/tree/main/docs/source_en\" target=\"_blank\">'
        'SWIFT Documentation</a> for more usages, Use SWIFT_UI_LANG=zh variable to switch to Chinese UI',
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
        def get_custom_css():
            p = os.path.join(os.path.dirname(__file__), 'style.css')
            if os.path.exists(p):
                with open(p, 'r', encoding='utf-8') as f:
                    return f.read()
            return ''
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
            gr.HTML(
                f"""
                <div class='topbar'>
                    <div class='brand'>
                        <div class='logo'>{logo_svg}</div>
                        <div class='titles'>
                            <div class='title'>新大陆大模型训练推理平台</div>
                            <div class='subtitle'>Newland AI Training & Inference Platform</div>
                        </div>
                    </div>
                    <div class='user'>
                        <span class='avatar'></span>
                        <span class='name'>admin</span>
                    </div>
                </div>
                """
            )
            with gr.Row():
                with gr.Column(scale=1, min_width=280, elem_classes="sidebar"):
                    gr.HTML(
                        f"""
                        <div class=\"sidebar-menu\">
                            <div class=\"sidebar-group-title\">模型训练</div>
                            <div id=\"train-submenu\" class=\"submenu\" style=\"display:block;\">
                                <div class=\"sidebar-menu-item inactive\" data-tab=\"llm_train\">
                                    <span class=\"menu-label\"><svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M4 6h16v2H4zM6 11h12v2H6zM8 16h8v2H8z\"/></svg>LLM预训练/微调</span>
                                </div>
                                <div class=\"sidebar-menu-item inactive\" data-tab=\"llm_rlhf\">
                                    <span class=\"menu-label\"><svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12 12c2.761 0 5-2.239 5-5s-2.239-5-5-5-5 2.239-5 5 2.239 5 5 5zm0 2c-3.866 0-7 3.134-7 7h14c0-3.866-3.134-7-7-7z\"/></svg>LLM人类对齐</span>
                                </div>
                                <div class=\"sidebar-menu-item inactive\" data-tab=\"llm_grpo\">
                                    <span class=\"menu-label\"><svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><circle cx=\"6\" cy=\"12\" r=\"2\"/><circle cx=\"12\" cy=\"12\" r=\"2\"/><circle cx=\"18\" cy=\"12\" r=\"2\"/></svg>LLM GRPO</span>
                                </div>
                            </div>
                            <div class=\"sidebar-group-title\">模型服务</div>
                            <div id=\"infer-submenu\" class=\"submenu\" style=\"display:block;\">
                                <div class=\"sidebar-menu-item inactive\" data-tab=\"llm_infer\">
                                    <span class=\"menu-label\"><svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12 2l4 4h-3v6h-2V6H8l4-4zm-7 18h14v2H5z\"/></svg>LLM推理</span>
                                </div>
                                <div class=\"sidebar-menu-item inactive\" data-tab=\"llm_export\">
                                    <span class=\"menu-label\"><svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12 3v10l4-4 1.41 1.41L12 16.83 6.59 10.41 8 9l4 4V3h0zM5 19h14v2H5z\"/></svg>LLM导出</span>
                                </div>
                            </div>
                            <div class=\"sidebar-group-title\">评测与演示</div>
                            <div id=\"eval-submenu\" class=\"submenu\" style=\"display:block;\">
                                <div class=\"sidebar-menu-item inactive\" data-tab=\"llm_eval\">
                                    <span class=\"menu-label\"><svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M5 17h3V7H5v10zm5 0h3V10h-3v7zm5 0h3V4h-3v13z\"/></svg>LLM评测</span>
                                </div>
                                <div class=\"sidebar-menu-item inactive\" data-tab=\"llm_sample\">
                                    <span class=\"menu-label\"><svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M7 5h10v2H7V5zm-2 6h14v2H5v-2zm3 6h8v2H8v-2z\"/></svg>LLM采样</span>
                                </div>
                            </div>
                        </div>
                        """,
                        elem_classes="no-frame",
                    )
                with gr.Column(scale=4, min_width=600, elem_classes="main-content"):
                    gr.HTML(
                        f"""
                        <div id='page-tag' class='page-tag'></div>
                        <div id='page-subtitle' class='page-subtitle'></div>
                        """
                    )
                    with gr.Tabs():
                        LLMTrain.build_ui(LLMTrain)
                        LLMRLHF.build_ui(LLMRLHF)
                        LLMGRPO.build_ui(LLMGRPO)
                        LLMInfer.build_ui(LLMInfer)
                        LLMExport.build_ui(LLMExport)
                        LLMEval.build_ui(LLMEval)
                        LLMSample.build_ui(LLMSample)

            concurrent = {}
            if version.parse(gr.__version__) < version.parse('4.0.0'):
                concurrent = {'concurrency_count': 5}
            app.load(
                partial(LLMTrain.update_input_model, arg_cls=RLHFArguments),
                inputs=[LLMTrain.element('model')],
                outputs=[LLMTrain.element('train_record')] + list(LLMTrain.valid_elements().values()))
            app.load(
                partial(LLMRLHF.update_input_model, arg_cls=RLHFArguments),
                inputs=[LLMRLHF.element('model')],
                outputs=[LLMRLHF.element('train_record')] + list(LLMRLHF.valid_elements().values()))
            app.load(
                partial(LLMGRPO.update_input_model, arg_cls=RLHFArguments),
                inputs=[LLMGRPO.element('model')],
                outputs=[LLMGRPO.element('train_record')] + list(LLMGRPO.valid_elements().values()))
            app.load(
                partial(LLMInfer.update_input_model, arg_cls=DeployArguments, has_record=False),
                inputs=[LLMInfer.element('model')],
                outputs=list(LLMInfer.valid_elements().values()))
            app.load(
                partial(LLMExport.update_input_model, arg_cls=ExportArguments, has_record=False),
                inputs=[LLMExport.element('model')],
                outputs=list(LLMExport.valid_elements().values()))
            app.load(
                partial(LLMEval.update_input_model, arg_cls=EvalArguments, has_record=False),
                inputs=[LLMEval.element('model')],
                outputs=list(LLMEval.valid_elements().values()))
            app.load(
                partial(LLMSample.update_input_model, arg_cls=SamplingArguments, has_record=False),
                inputs=[LLMSample.element('model')],
                outputs=list(LLMSample.valid_elements().values()))
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
                        if (tab) { tab.click(); }
                    }
                    window.selectMenu = function(tabId, elem) {
                        var subItems = document.querySelectorAll('.submenu .sidebar-menu-item');
                        for (var s = 0; s < subItems.length; s++) { subItems[s].classList.remove('active'); subItems[s].classList.add('inactive'); }
                        if (elem) { elem.classList.add('active'); elem.classList.remove('inactive'); }
                        var tag = document.getElementById('page-tag');
                        if (tag) {
                            var text = '';
                            if (elem) {
                                var sp = elem.querySelector('span');
                                text = sp ? sp.innerText : elem.innerText;
                            }
                            tag.textContent = text;
                        }
                        var sub = document.getElementById('page-subtitle');
                        if (sub) {
                            var dm = {
                                'llm_train': '\u914D\u7F6E\u60A8\u7684LLM\u6A21\u578B\u3001\u6570\u636E\u96C6\u548C\u8BAD\u7EC3\u53C2\u6570\u3002',
                                'llm_rlhf': '\u8BBE\u7F6E\u4EBA\u7C7B\u53CD\u9988\u5BF9\u9F50\u53C2\u6570\u4E0E\u6D41\u7A0B\u3002',
                                'llm_grpo': '\u914D\u7F6EGRPO\u5F3A\u5316\u5B66\u4E60\u76F8\u5173\u8BBE\u7F6E\u3002',
                                'llm_infer': '\u542F\u52A8\u6216\u914D\u7F6E\u6A21\u578B\u63A8\u7406\u670D\u52A1\u3002',
                                'llm_export': '\u5C06\u6A21\u578B\u5BFC\u51FA\u4E3A\u90E8\u7F72\u683C\u5F0F\u3002',
                                'llm_eval': '\u8FDB\u884C\u6A21\u578B\u8BC4\u6D4B\u4E0E\u5BF9\u6BD4\u3002',
                                'llm_sample': '\u4EA4\u4E92\u5F0F\u91C7\u6837\u4E0E\u793A\u4F8B\u6F14\u793A\u3002'
                            };
                            sub.textContent = dm[tabId] || '';
                        }
                        var panel = document.getElementById(tabId);
                        if (panel) {
                            var container = panel.parentElement;
                            if (container) {
                                var allPanels = container.querySelectorAll('.tabitem');
                                for (var i = 0; i < allPanels.length; i++) { allPanels[i].style.display = 'none'; }
                            }
                            panel.style.display = 'block';
                        } else {
                            clickTabImpl(tabId);
                        }
                    };
                    var menu = document.querySelector('.sidebar-menu');
                    if (menu) {
                        menu.addEventListener('click', function(e){
                            var leaf = e.target.closest('.sidebar-menu .submenu .sidebar-menu-item');
                            if (leaf && leaf.dataset && leaf.dataset.tab) { window.selectMenu(leaf.dataset.tab, leaf); return; }
                        });
                    }
                    var wrapper = document.querySelector('.main-content .tab-wrapper');
                    if (wrapper) {
                        var tabs = wrapper.querySelectorAll('.tab-container, .overflow-menu');
                        tabs.forEach(function(el){ el.remove(); });
                        wrapper.remove();
                    }
                    var defaultLeaf = document.querySelector(".submenu .sidebar-menu-item[data-tab='llm_train']");
                    if (defaultLeaf) { window.selectMenu('llm_train', defaultLeaf); }
                    var opt = document.getElementById('optimizer_params');
                    if (opt) {
                        var accBtn = opt.previousElementSibling;
                        if (accBtn && accBtn.tagName.toLowerCase() === 'button') { accBtn.click(); }
                        var galoreTab = opt.querySelector('[aria-controls*="galore_tab"]') || opt.querySelector('button[data-testid*="galore_tab"]');
                        if (galoreTab) { galoreTab.click(); }
                    }
                }
                """
            app.load(None, None, None, js=js_script())
        app.queue(**concurrent).launch(server_name=server, inbrowser=True, server_port=port, height=800, share=share)


def webui_main(args: Optional[Union[List[str], WebUIArguments]] = None):
    return SwiftWebUI(args).main()
