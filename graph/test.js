cytoscape({
  container: document.getElementById('cy'),
  elements:[
    {
      group:'nodes',

      data:{
        id:'n1',
        parent:'nparent',
        weight: 100
      },

      //scratchpad data
      scratch:{
        foo:'bar'
      },

      position:{
        x:100, y:100
      },

      selected: false,

      selectable: true,

      locked: false,

      grabbable:true,

      classes:'foo bar',

      style:{'background-color':'red'},


    },

    {
      group: 'nodes',
      data:{
        id:'n2'
      },
      renderedPosition:{x:200, y:200}
    },

    {
      group: 'nodes',
      data:{id:'n3', parent:'nparent'},
      position:{x:123, y:234}
    },
    { // edge e1
      group: 'edges',
      data: {
        id: 'e1',
        source: 'n1', // the source node id (edge comes from this node)
        target: 'n2'  // the target node id (edge goes to this node)
      }
    }
  ],

  layout: {
   name: 'preset'
 },

 // so we can see the ids
 style: [
   {
     selector: 'node',
     style: {
       'content': 'data(id)'
     }
   }
 ]
});
