<template>
    <div v-if="status=='loading'">
        <div class="spin"></div>
    </div>
    <div v-else-if="status=='error'">
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="red" class="bi bi-bug" viewBox="0 0 16 16">
  <path d="M4.355.522a.5.5 0 0 1 .623.333l.291.956A4.979 4.979 0 0 1 8 1c1.007 0 1.946.298 2.731.811l.29-.956a.5.5 0 1 1 .957.29l-.41 1.352A4.985 4.985 0 0 1 13 6h.5a.5.5 0 0 0 .5-.5V5a.5.5 0 0 1 1 0v.5A1.5 1.5 0 0 1 13.5 7H13v1h1.5a.5.5 0 0 1 0 1H13v1h.5a1.5 1.5 0 0 1 1.5 1.5v.5a.5.5 0 1 1-1 0v-.5a.5.5 0 0 0-.5-.5H13a5 5 0 0 1-10 0h-.5a.5.5 0 0 0-.5.5v.5a.5.5 0 1 1-1 0v-.5A1.5 1.5 0 0 1 2.5 10H3V9H1.5a.5.5 0 0 1 0-1H3V7h-.5A1.5 1.5 0 0 1 1 5.5V5a.5.5 0 0 1 1 0v.5a.5.5 0 0 0 .5.5H3c0-1.364.547-2.601 1.432-3.503l-.41-1.352a.5.5 0 0 1 .333-.623zM4 7v4a4 4 0 0 0 3.5 3.97V7H4zm4.5 0v7.97A4 4 0 0 0 12 11V7H8.5zM12 6a3.989 3.989 0 0 0-1.334-2.982A3.983 3.983 0 0 0 8 2a3.983 3.983 0 0 0-2.667 1.018A3.989 3.989 0 0 0 4 6h8z"/>
        </svg>
        <p>Something went wrong...</p>
    </div>
    <div v-else="">
        <file-tree :node="files" @node_clicked="node_clicked"></file-tree>
        <prism-editor v-if="code.length" class="code-editor" v-model="code" :language="language" :readonly="true" :lineNumbers="true" :highlight="highlighter"></prism-editor>
    </div>
</template>

<script>
import FileTree from './FileTree.vue';

import { PrismEditor } from 'vue-prism-editor';
import "vue-prism-editor/dist/prismeditor.min.css";

import { highlight, languages } from "prismjs/components/prism-core";
import "prismjs/components/prism-clike";
import "prismjs/components/prism-javascript";
import "prismjs/themes/prism-tomorrow.css";

import axios from 'axios';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
    name: "editor",
    components: { FileTree, PrismEditor, },
    data: function() { 
        return {
            'status': 'loading',
            'files': [],
            'code': '',
            'language': '',
        };
    },
    methods: {
        node_clicked: function(uuid) {
            axios.get('api/files/'+uuid)
                .then((response) => {
                    if ('contents' in response.data) {
                        this.code = response.data.contents;
                        this.language = response.data.language;
                    } else {
                        this.code = '';
                        this.language = '';
                    }
                })
                .catch((error) => {
                    this.status = 'error';
                    console.log(error);
                });
        },
        highlighter: function(code) {
            return highlight(code, languages.js);
        }
    },
    mounted() {
        axios.get('api/files/')
            .then((response) => {
                this.files = response.data.files;
                this.status = 'running';
            })
            .catch((error) => {
                this.status = 'error';
                console.log(error);
            });
    },
}
</script>

<style scoped>
@keyframes spinner {
    0% {
        transform: translate3d(-50%, -50%, 0) rotate(0deg);
    }
    100% {
        transform: translate3d(-50%, -50%, 0) rotate(360deg);
    }
}
.spin::before {
    animation: 1.5s linear infinite spinner;
    animation-play-state: inherit;
    border: solid 5px #ffa500;
    border-bottom-color: #1c87c9;
    border-radius: 50%;
    content: "";
    height: 40px;
    width: 40px;
    position: absolute;
    top: 10%;
    left: 10%;
    transform: translate3d(-50%, -50%, 0);
    will-change: transform;
}

.code-editor {
  background: #2d2d2d;
  color: #ccc;

  font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
  padding: 5px;
}
</style>
