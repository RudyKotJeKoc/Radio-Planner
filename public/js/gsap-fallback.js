/**
 * GSAP Fallback Implementation
 * Provides minimal GSAP API compatibility when external CDN fails
 */

// Create a minimal GSAP object with basic animation capabilities
window.gsap = {
    // Basic timeline implementation
    timeline: function(options = {}) {
        return {
            paused: options.paused || false,
            to: function(target, props) {
                this._animate(target, props);
                return this;
            },
            from: function(target, props) {
                this._animate(target, props);
                return this;
            },
            fromTo: function(target, fromProps, toProps) {
                this._animate(target, toProps);
                return this;
            },
            set: function(target, props) {
                const elements = typeof target === 'string' ? document.querySelectorAll(target) : [target];
                elements.forEach(el => {
                    if (el) {
                        Object.assign(el.style, this._convertProps(props));
                    }
                });
                return this;
            },
            play: function() {
                this.paused = false;
                return this;
            },
            pause: function() {
                this.paused = true;
                return this;
            },
            reverse: function() {
                return this;
            },
            restart: function() {
                return this;
            },
            _animate: function(target, props) {
                const elements = typeof target === 'string' ? document.querySelectorAll(target) : [target];
                const duration = (props.duration || 1) * 1000;
                const delay = (props.delay || 0) * 1000;
                
                elements.forEach(el => {
                    if (el) {
                        setTimeout(() => {
                            el.style.transition = `all ${duration}ms ease`;
                            Object.assign(el.style, this._convertProps(props));
                            
                            if (props.onComplete) {
                                setTimeout(props.onComplete, duration);
                            }
                        }, delay);
                    }
                });
            },
            _convertProps: function(props) {
                const cssProps = {};
                
                // Convert GSAP properties to CSS properties
                if (props.x !== undefined) cssProps.transform = `translateX(${props.x}px)`;
                if (props.y !== undefined) cssProps.transform = (cssProps.transform || '') + ` translateY(${props.y}px)`;
                if (props.opacity !== undefined) cssProps.opacity = props.opacity;
                if (props.scale !== undefined) cssProps.transform = (cssProps.transform || '') + ` scale(${props.scale})`;
                if (props.rotation !== undefined) cssProps.transform = (cssProps.transform || '') + ` rotate(${props.rotation}deg)`;
                
                // Direct CSS properties
                ['width', 'height', 'backgroundColor', 'color'].forEach(prop => {
                    if (props[prop] !== undefined) cssProps[prop] = props[prop];
                });
                
                return cssProps;
            }
        };
    },
    
    // Static animation methods
    to: function(target, props) {
        return this.timeline().to(target, props);
    },
    
    from: function(target, props) {
        return this.timeline().from(target, props);
    },
    
    fromTo: function(target, fromProps, toProps) {
        return this.timeline().fromTo(target, fromProps, toProps);
    },
    
    set: function(target, props) {
        return this.timeline().set(target, props);
    },
    
    // Plugin registration (no-op)
    registerPlugin: function() {
        return this;
    }
};

// Create Draggable plugin stub
window.Draggable = {
    create: function(target, options = {}) {
        const elements = typeof target === 'string' ? document.querySelectorAll(target) : [target];
        
        elements.forEach(el => {
            if (el) {
                let isDragging = false;
                let startX = 0, startY = 0;
                let currentX = 0, currentY = 0;
                
                el.addEventListener('mousedown', (e) => {
                    isDragging = true;
                    startX = e.clientX - currentX;
                    startY = e.clientY - currentY;
                    el.style.cursor = 'grabbing';
                });
                
                document.addEventListener('mousemove', (e) => {
                    if (!isDragging) return;
                    
                    e.preventDefault();
                    currentX = e.clientX - startX;
                    currentY = e.clientY - startY;
                    
                    el.style.transform = `translate(${currentX}px, ${currentY}px)`;
                });
                
                document.addEventListener('mouseup', () => {
                    isDragging = false;
                    el.style.cursor = 'grab';
                });
            }
        });
        
        return {
            disable: function() {},
            enable: function() {},
            kill: function() {}
        };
    }
};

// Create MotionPathPlugin stub
window.MotionPathPlugin = {};

console.log('[GSAP Fallback] Fallback implementation loaded');