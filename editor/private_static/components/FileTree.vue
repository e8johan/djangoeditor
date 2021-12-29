<template>
  <li class="node-tree">
    <a v-on:click="$emit('node_clicked', node.uuid)">{{ node.label }}</a>
    <ul v-if="node.children && node.children.length">
      <node v-for="child in node.children" :node="child" v-on="$listeners"></node>
    </ul>
  </li>
</template>

<script>
export default {
  name: "node",
  props: {
    node: Object
  }
};
</script>
