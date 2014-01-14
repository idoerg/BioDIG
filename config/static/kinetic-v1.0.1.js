/**
 * Kinetic JS JavaScript Library v1.0.1
 * http://www.kineticjs.com/
 * Copyright 2011, Eric Rowell
 * Licensed under the MIT or GPL Version 2 licenses.
 * Date: Jun 7 2011
 *
 * Copyright (C) 2011 by Eric Rowell
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var Kinetic = {};

Kinetic.Stage = function(canvas){
    // Stage vars
    this.canvas = canvas;
    this.fps = 60;
    this.context = canvas.getContext("2d");
    this.updateStage = undefined;
    this.drawStage = undefined;
    
    // Event vars
    this.mousePos = null;
    this.mouseDown = false;
    this.mouseUp = false;
    this.currentRegion = null;
    this.regionCounter = 0;
    this.lastRegionIndex = null;
    
    // Animation vars
    this.t = 0;
    this.timeInterval = 1000 / this.fps;
    this.intervalId = null;
    this.frame = 0;
};

// Stage
Kinetic.Stage.prototype.isMousedown = function(){
    return this.mouseDown;
};
Kinetic.Stage.prototype.isMouseup = function(){
    return this.mouseUp;
};
Kinetic.Stage.prototype.setDrawStage = function(func){
    this.drawStage = func;
    this.listen();
};
Kinetic.Stage.prototype.drawStage = function(){
    if (this.drawStage !== undefined) {
        this.clearCanvas();
        this.drawStage();
    }
};
Kinetic.Stage.prototype.setUpdateStage = function(func){
    this.updateStage = func;
};
Kinetic.Stage.prototype.getContext = function(){
    return this.context;
};
Kinetic.Stage.prototype.clearCanvas = function(){
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
};

// Events
Kinetic.Stage.prototype.listen = function(){
    // store current listeners
    var that = this;
    var canvasOnmouseover = this.canvas.onmouseover;
    var canvasOnmouseout = this.canvas.onmouseout;
    var canvasOnmousemove = this.canvas.onmousemove;
    var canvasOnmousedown = this.canvas.onmousedown;
    var canvasOnmouseup = this.canvas.onmouseup;
    
    if (this.drawStage !== undefined) {
        this.drawStage();
    }
    
    this.canvas.onmouseover = function(e){
        if (!e) {
            e = window.event;
        }
        
        that.setMousePosition(e);
        if (typeof(canvasOnmouseover) == typeof(Function)) {
            canvasOnmouseover();
        }
    };
    this.canvas.onmouseout = function(){
        that.mousePos = null;
        if (typeof(canvasOnmouseout) == typeof(Function)) {
            canvasOnmouseout();
        }
    };
    this.canvas.onmousemove = function(e){
        if (!e) {
            e = window.event;
        }
        that.reset(e);
        
        if (typeof(canvasOnmousemove) == typeof(Function)) {
            canvasOnmousemove();
        }
    };
    this.canvas.onmousedown = function(e){
        if (!e) {
            e = window.event;
        }
        that.mouseDown = true;
        that.reset(e);
        
        if (typeof(canvasOnmousedown) == typeof(Function)) {
            canvasOnmousedown();
        }
    };
    this.canvas.onmouseup = function(e){
        if (!e) {
            e = window.event;
        }
        that.mouseUp = true;
        that.reset(e);
        
        if (typeof(canvasOnmouseup) == typeof(Function)) {
            canvasOnmouseup();
        }
    };
};
Kinetic.Stage.prototype.beginRegion = function(){
    this.currentRegion = {};
    this.regionCounter++;
};
Kinetic.Stage.prototype.addRegionEventListener = function(type, func){
    if (type == "onmouseover") {
        this.currentRegion.onmouseover = func;
    }
    else if (type == "onmouseout") {
        this.currentRegion.onmouseout = func;
    }
    else if (type == "onmousemove") {
        this.currentRegion.onmousemove = func;
    }
    else if (type == "onmousedown") {
        this.currentRegion.onmousedown = func;
    }
    else if (type == "onmouseup") {
        this.currentRegion.onmouseup = func;
    }
};
Kinetic.Stage.prototype.closeRegion = function(){
    if (this.mousePos !== null && this.context.isPointInPath(this.mousePos.x, this.mousePos.y)) {
    
        // handle onmousemove
        // do this everytime
        if (this.currentRegion.onmousemove !== undefined) {
            this.currentRegion.onmousemove();
        }
        
        // handle onmouseover
        if (this.lastRegionIndex != this.regionCounter) {
            this.lastRegionIndex = this.regionCounter;
            
            if (this.currentRegion.onmouseover !== undefined) {
                this.currentRegion.onmouseover();
            }
        }
        
        // handle onmousedown
        if (this.mouseDown && this.currentRegion.onmousedown !== undefined) {
            this.currentRegion.onmousedown();
            this.mouseDown = false;
        }
        
        // handle onmouseup
        if (this.mouseUp && this.currentRegion.onmouseup !== undefined) {
            this.currentRegion.onmouseup();
            this.mouseUp = false;
        }
        
    }
    else if (this.regionCounter == this.lastRegionIndex) {
        // handle mouseout condition
        this.lastRegionIndex = null;
        
        if (this.currentRegion.onmouseout !== undefined) {
            this.currentRegion.onmouseout();
        }
    }
    
    this.regionCounter++;
};
Kinetic.Stage.prototype.getMousePos = function(evt){
    return this.mousePos;
};
Kinetic.Stage.prototype.setMousePosition = function(evt){       
    var mouseX = evt.clientX - this.canvas.offsetLeft + window.pageXOffset;
    var mouseY = evt.clientY - this.canvas.offsetTop + window.pageYOffset;
    this.mousePos = {
        x: mouseX,
        y: mouseY
    };
};

Kinetic.Stage.prototype.reset = function(evt){
    this.setMousePosition(evt);
    this.regionCounter = 0;
    
    if (this.drawStage !== undefined) {
        this.clearCanvas();
        this.drawStage();
    }
    
    this.mouseDown = false;
    this.mouseUp = false;
};

// Animation
Kinetic.Stage.prototype.getFrame = function(){
    return this.frame;
};
Kinetic.Stage.prototype.start = function(){
    var that = this;
    if (this.drawStage !== undefined) {
        this.drawStage();
    }
    this.intervalId = setInterval(function(){
        that.animationLoop();
    }, this.timeInterval);
};
Kinetic.Stage.prototype.stop = function(){
    this.clearInterval(intervalId);
};
Kinetic.Stage.prototype.getTimeInterval = function(){
    return this.timeInterval;
};
Kinetic.Stage.prototype.getTime = function(){
    return this.t;
};
Kinetic.Stage.prototype.animationLoop = function(){
    this.frame++;
    this.t += this.timeInterval;
    this.clearCanvas();
    if (this.updateStage !== undefined) {
        this.updateStage();
    }
    if (this.drawStage !== undefined) {
        this.drawStage();
    }
};

