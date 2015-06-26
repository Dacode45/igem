//functions that aren't really integral to the graph, but are necessary to support devices

function isTouchDevice(){
  return 'ontouchstart' in window // works on most browsers
        || 'onmsgesturechange' in window; // works on ie10
}

function objToArray(obj){
  if(Array.isArray(obj))
    return obj;
  return Object.keys(obj).map(function(key){return obj[key]});
}


//actual code
function redactData(str){
  var illegalWords = [
    {word:"pa2c_tesA", replace:"plasmid"}
  ]

  illegalWords.forEach(function(word){
    var replaceWith = word.replace || "[REDACTED]"
    str = str.replace(word.word, replaceWith)
  });
  return JSON.parse(str)
}

function awake(){
  //load journals
  var manifest = ["charlotte.json"]
  var count = 0;
  var journals = Array(manifest.length)
  var failedToLoad = 0;
  function loadManifest(data){
    //console.log(arguments)
    journals[count] = data
    count++;
    if(count == manifest.length - failedToLoad){
      start(journals);
    }
  }

  manifest.forEach(function(file){
    $.ajax({
      type:"GET",
      contentType:"application/json",
      url:"../Journal/" + file + "?action=raw&ctype=text/javascript",
      success:function(data){
          loadManifest(redactData(JSON.stringify(data)));
      },
      error:function(e){
        failedToLoad++;
        console.log("Failed to load a journal", e)
      }

    })

  })
}

function start(journals){
  console.log(journals)
  var options = {
    container: document.getElementById("cy"),
    //elements
    //style
    layout:{name:'grid'},
    ready:function(evt){
      graphReady(evt)
    },
    zoom:1,
    pan:{x:0,y:0},
    minZoom:1e-50,
    maxZoom:1e50,
    zoomingEnabled:true,
    userZoomingEnabled:true,
    panningEnabled:true,
    userPanningEnabled:true,
    boxSelectionEnabled:true,
    selectionType:(isTouchDevice?'additive':'single'),
    touchTapThreshold:8,
    desktopTapThreshold:4,
    autolock:false,
    autoungrabify:false,
    autounselectify:false,

    //rendering options
    headless:false,
    styleEnabled:true,
    hideEdgesOnViewport:false,
    hideLabelsOnViewport:false,
    textureOnViewport:false,
    motionBlur:true,
    motionBlurOpacity:.2,
    wheelSensitivity:1,
    pixelRatio:1,
    initrender:function(evt){
      graphRenderReady(evt);
    },
    renderer:{}
  };
  //convert journals into graph for Cyoscape
  var elements = journalsToGraph(journals); //{nodes:[], edges:[]}
  //console.log(elements)
  options.elements = elements;

  this.cy = cytoscape(options);
}

function journalsToGraph(journals){
  //journals are organized into an array of events that happend on a given day.
  var nodes = {};
  var edges = {};
  var jns = journals[0] //journals = [Array(9)]

  nodeCount = 0;
  edgeCount = 0;

  for(var d = 0; d < jns.length; d++){
    var journal = jns[d];
    //console.log(journal)
    var date = Date.parse(journal["when"]);
    var exps = journal["what"];

    //get an experiment
    for(var i = 0; i < exps.length; i++){
      var exp = exps[i];
      var node = {};
      node.data = {};
      //check for fields.
      if(exp.hasOwnProperty('id')){
        node.data.id = exp['id'];
      }else {
        continue;
      }

      nodeCount++;

      //from
      if(exp.hasOwnProperty('from')){
        var sources = Array.isArray(exp['from'])? exp['from'] : [exp['from']];
        sources.forEach(function(id){
          edges[id+"_"+node.data.id] = {
            data:{
              id:id+"_"+node.data.id,
              source:id,
              target:node.data.id
            }
          }
          console.log(id+"_"+node.data.id)
          edgeCount++;
        });

      }



      //add to nodes list
      nodes[node.data.id] = node;
      console.log(node, node.data.id)
    }

  }
  return {nodes:objToArray(nodes), edges:objToArray(edges) }
}


function graphRenderReady(evt){
  //grab screenshot
}

function graphReady(evt){
  console.log("Graph Ready", evt)
}

$(document).ready(function(){
  awake();
});



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
