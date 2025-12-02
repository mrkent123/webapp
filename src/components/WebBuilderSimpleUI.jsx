import React, { useState, useRef, useCallback } from 'react';
import './webbuilder.skin.css';

// HMR Test - File modified to trigger hot reload
const WebBuilderSimpleUI = () => {
  // Draggable elements
  const draggableElements = [
    { type: 'section', label: 'Section', icon: '▭', defaultProps: { padding: '20px', margin: '10px' } },
    { type: 'heading', label: 'Heading', icon: 'H', defaultProps: { text: 'Heading', fontSize: '24px', fontWeight: 'bold' } },
    { type: 'text', label: 'Text', icon: 'T', defaultProps: { text: 'Sample text content', fontSize: '16px' } },
    { type: 'image', label: 'Image', icon: '🖼️', defaultProps: { src: 'https://placehold.co/300x200', alt: 'Placeholder image' } },
    { type: 'button', label: 'Button', icon: '🔘', defaultProps: { text: 'Button', padding: '10px 20px', backgroundColor: '#3b82f6', color: '#ffffff' } }
  ];

  // State for the schema and UI
  const [schema, setSchema] = useState([
    {
      id: 'root-section-1',
      type: 'section',
      props: { padding: '20px', margin: '10px', backgroundColor: '#f9fafb' },
      children: []
    }
  ]);
  
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [previewMode, setPreviewMode] = useState('mobile'); // 'desktop' or 'mobile'
  const dragItem = useRef(null);
  const dragNode = useRef(null);

  // Get selected node from schema
  const getSelectedNode = useCallback(() => {
    if (!selectedNodeId) return null;
    
    const findNode = (nodes) => {
      for (const node of nodes) {
        if (node.id === selectedNodeId) return node;
        if (node.children && node.children.length) {
          const found = findNode(node.children);
          if (found) return found;
        }
      }
      return null;
    };
    
    return findNode(schema);
  }, [schema, selectedNodeId]);

  // Handle drag start
  const handleDragStart = (e, element) => {
    dragItem.current = { ...element, id: `new-${Date.now()}` };
    e.dataTransfer.effectAllowed = 'copy';
  };

  // Handle drop on canvas
  const handleDrop = (e, targetNodeId = null) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (!dragItem.current) return;

    const newElement = {
      id: dragItem.current.id,
      type: dragItem.current.type,
      props: { ...dragItem.current.defaultProps },
      children: []
    };

    if (targetNodeId) {
      // Add as child of target node
      setSchema(prevSchema => {
        const updateChildren = (nodes) => {
          return nodes.map(node => {
            if (node.id === targetNodeId) {
              return {
                ...node,
                children: [...node.children, newElement]
              };
            } else if (node.children && node.children.length) {
              return {
                ...node,
                children: updateChildren(node.children)
              };
            }
            return node;
          });
        };
        return updateChildren(prevSchema);
      });
    } else {
      // Add as top-level element
      setSchema(prevSchema => [...prevSchema, newElement]);
    }

    dragItem.current = null;
  };

  // Handle drop on existing element
  const handleElementDrop = (e, targetNodeId) => {
    e.preventDefault();
    e.stopPropagation();
    handleDrop(e, targetNodeId);
  };

  // Handle property changes
  const handlePropChange = (propName, value) => {
    if (!selectedNodeId) return;

    setSchema(prevSchema => {
      const updateNodeProps = (nodes) => {
        return nodes.map(node => {
          if (node.id === selectedNodeId) {
            return {
              ...node,
              props: {
                ...node.props,
                [propName]: value
              }
            };
          } else if (node.children && node.children.length) {
            return {
              ...node,
              children: updateNodeProps(node.children)
            };
          }
          return node;
        });
      };
      return updateNodeProps(prevSchema);
    });
  };

  // Delete selected node
  const handleDeleteNode = () => {
    if (!selectedNodeId) return;

    setSchema(prevSchema => {
      const removeNode = (nodes) => {
        return nodes.filter(node => {
          if (node.id === selectedNodeId) {
            return false;
          }
          if (node.children && node.children.length) {
            node.children = removeNode(node.children);
          }
          return true;
        });
      };
      return removeNode(prevSchema);
    });
    
    setSelectedNodeId(null);
  };

  // Render element based on type
  const renderElement = (element, depth = 0) => {
    const isSelected = selectedNodeId === element.id;
    const selectedNode = getSelectedNode();
    const isElementSelected = selectedNode && selectedNode.id === element.id;
    
    const baseStyle = {
      position: 'relative',
      margin: '5px',
      padding: '5px',
      border: isElementSelected ? '2px solid #3b82f6' : '1px dashed #d1d5db',
      backgroundColor: isElementSelected ? 'rgba(59, 130, 246, 0.1)' : 'transparent',
      minHeight: '40px',
      transition: 'border 0.2s, background-color 0.2s'
    };

    const commonProps = {
      key: element.id,
      style: baseStyle,
      onClick: (e) => {
        e.stopPropagation();
        setSelectedNodeId(element.id);
      },
      onDragOver: (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
      },
      onDrop: (e) => handleElementDrop(e, element.id),
      role: 'region',
      'aria-label': `${element.type} element`,
      'aria-selected': isElementSelected
    };

    switch (element.type) {
      case 'section':
        return (
          <div 
            {...commonProps}
            style={{
              ...baseStyle,
              ...element.props
            }}
          >
            <div style={{ padding: '2px', fontSize: '12px', color: '#6b7280', marginBottom: '5px' }}>
              Section
            </div>
            {element.children && element.children.map(child => renderElement(child, depth + 1))}
            <div 
              style={{ 
                minHeight: '30px', 
                border: '1px dashed #cbd5e1', 
                borderRadius: '4px',
                margin: '5px 0' 
              }}
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => handleElementDrop(e, element.id)}
            />
          </div>
        );
      
      case 'heading':
        return (
          <h2 
            {...commonProps}
            style={{
              ...baseStyle,
              fontSize: element.props.fontSize || '24px',
              fontWeight: element.props.fontWeight || 'bold',
              textAlign: element.props.align || 'left',
              color: element.props.color || '#1f2937',
              margin: '10px 0'
            }}
          >
            {element.props.text || 'Heading'}
          </h2>
        );
      
      case 'text':
        return (
          <p 
            {...commonProps}
            style={{
              ...baseStyle,
              fontSize: element.props.fontSize || '16px',
              textAlign: element.props.align || 'left',
              color: element.props.color || '#374151',
              lineHeight: element.props.lineHeight || '1.5',
              margin: '10px 0'
            }}
          >
            {element.props.text || 'Sample text content'}
          </p>
        );
      
      case 'image':
        return (
          <div 
            {...commonProps}
            style={{ ...baseStyle, textAlign: 'center' }}
          >
            <img
              src={element.props.src || 'https://placehold.co/300x200'}
              alt={element.props.alt || 'Placeholder image'}
              style={{
                width: element.props.width || '100%',
                height: element.props.height || 'auto',
                borderRadius: element.props.borderRadius || '0',
                maxWidth: '100%',
                objectFit: 'cover'
              }}
            />
          </div>
        );
      
      case 'button':
        return (
          <button
            {...commonProps}
            style={{
              ...baseStyle,
              backgroundColor: element.props.backgroundColor || '#3b82f6',
              color: element.props.color || '#ffffff',
              padding: element.props.padding || '10px 20px',
              borderRadius: element.props.borderRadius || '6px',
              border: 'none',
              cursor: 'pointer',
              fontSize: element.props.fontSize || '16px',
              margin: '10px 0',
              fontWeight: '500'
            }}
          >
            {element.props.text || 'Button'}
          </button>
        );
      
      default:
        return (
          <div 
            {...commonProps}
            style={{ ...baseStyle, fontStyle: 'italic', color: '#9ca3af' }}
          >
            Unknown element type: {element.type}
          </div>
        );
    }
  };

  // Export schema as JSON
  const exportSchema = () => {
    const dataStr = JSON.stringify(schema, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = 'web-builder-schema.json';
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  // Export HTML to console
  const exportToHTML = () => {
    console.log('Schema for HTML export:', JSON.stringify(schema, null, 2));
    
    // Simple HTML representation for preview
    const htmlString = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exported Web Builder Content</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
    .section { padding: 20px; margin: 10px; }
    .heading { font-size: 24px; font-weight: bold; margin: 10px 0; }
    .text { font-size: 16px; margin: 10px 0; }
    .button { padding: 10px 20px; background-color: #3b82f6; color: white; border: none; border-radius: 6px; cursor: pointer; }
  </style>
</head>
<body>
  ${generateHTMLFromSchema(schema)}
</body>
</html>`;

    console.log('HTML preview:', htmlString);
    alert('Schema and HTML preview logged to console. Check browser console for details.');
  };

  // Helper function to generate HTML from schema
  const generateHTMLFromSchema = (nodes) => {
    return nodes.map(node => {
      switch (node.type) {
        case 'section':
          return `<div class="section" style="${generateStyleString(node.props)}">
            ${node.children && node.children.length ? generateHTMLFromSchema(node.children) : ''}
          </div>`;
        case 'heading':
          return `<h2 class="heading" style="${generateStyleString(node.props)}">${node.props.text || 'Heading'}</h2>`;
        case 'text':
          return `<p class="text" style="${generateStyleString(node.props)}">${node.props.text || 'Sample text content'}</p>`;
        case 'button':
          return `<button class="button" style="${generateStyleString(node.props)}">${node.props.text || 'Button'}</button>`;
        case 'image':
          return `<img src="${node.props.src || 'https://placehold.co/300x200'}" alt="${node.props.alt || 'Placeholder image'}" style="${generateStyleString(node.props)}" />`;
        default:
          return '';
      }
    }).join('\n');
  };

  // Helper function to convert props to CSS string
  const generateStyleString = (props) => {
    if (!props) return '';
    
    return Object.entries(props)
      .filter(([key, value]) => typeof value !== 'object' && typeof value !== 'undefined' && value !== null)
      .map(([key, value]) => {
        const kebabKey = key.replace(/([A-Z])/g, '-$1').toLowerCase();
        return `${kebabKey}: ${value};`;
      })
      .join(' ');
  };

  // Handle keyboard events
  const handleKeyDown = (e) => {
    if (e.key === 'Delete' && selectedNodeId) {
      handleDeleteNode();
    }
  };

  // Get the selected node for the properties panel
  const selectedNode = getSelectedNode();

  return (
    <div 
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        backgroundColor: '#f3f4f6',
        fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif',
        overflow: 'hidden',
        position: 'relative'
      }}
      onKeyDown={handleKeyDown}
      tabIndex={0}
    >
      {/* Top toolbar */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '12px 16px',
        backgroundColor: '#ffffff',
        borderBottom: '1px solid #e5e7eb',
        zIndex: 10
      }}>
        <h1 style={{ fontSize: '18px', fontWeight: '600', margin: 0, color: '#1f2937' }}>
          Web Builder
        </h1>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            onClick={() => setPreviewMode(previewMode === 'mobile' ? 'desktop' : 'mobile')}
            style={{
              padding: '8px 12px',
              borderRadius: '6px',
              border: '1px solid #d1d5db',
              backgroundColor: '#ffffff',
              cursor: 'pointer',
              fontSize: '14px',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
            aria-label={previewMode === 'mobile' ? 'Switch to desktop view' : 'Switch to mobile view'}
          >
            {previewMode === 'mobile' ? '📱 Mobile' : '🖥️ Desktop'}
          </button>
          <button
            onClick={exportSchema}
            style={{
              padding: '8px 12px',
              borderRadius: '6px',
              backgroundColor: '#3b82f6',
              color: '#ffffff',
              border: 'none',
              cursor: 'pointer',
              fontSize: '14px'
            }}
            aria-label="Export schema as JSON"
          >
            Download JSON
          </button>
          <button
            onClick={exportToHTML}
            style={{
              padding: '8px 12px',
              borderRadius: '6px',
              backgroundColor: '#10b981',
              color: '#ffffff',
              border: 'none',
              cursor: 'pointer',
              fontSize: '14px'
            }}
            aria-label="Export HTML to console"
          >
            Console HTML
          </button>
        </div>
      </div>

      {/* Main content */}
      <div style={{
        display: 'flex',
        flex: 1,
        overflow: 'hidden'
      }}>
        {/* Left toolbox */}
        <div 
          style={{
            width: '240px',
            backgroundColor: '#ffffff',
            borderRight: '1px solid #e5e7eb',
            padding: '16px',
            display: 'flex',
            flexDirection: 'column',
            overflowY: 'auto'
          }}
          aria-label="Toolbox panel"
        >
          <h2 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px', color: '#374151' }}>
            Elements
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {draggableElements.map((element) => (
              <div
                key={element.type}
                draggable
                onDragStart={(e) => handleDragStart(e, element)}
                style={{
                  padding: '10px',
                  border: '1px solid #d1d5db',
                  borderRadius: '6px',
                  backgroundColor: '#f9fafb',
                  cursor: 'move',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  transition: 'all 0.2s'
                }}
                onMouseDown={(e) => e.preventDefault()} // Prevent text selection while dragging
                aria-label={`Draggable ${element.label}`}
              >
                <span style={{ fontSize: '16px' }}>{element.icon}</span>
                <span style={{ fontSize: '14px' }}>{element.label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Center canvas */}
        <div 
          style={{
            flex: 1,
            padding: '20px',
            overflow: 'auto',
            backgroundColor: '#f9fafb',
            display: 'flex',
            justifyContent: 'center',
            position: 'relative'
          }}
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleDrop}
          onClick={() => setSelectedNodeId(null)}
          role="main"
          aria-label="Canvas area"
        >
          <div
            style={{
              width: previewMode === 'mobile' ? '393px' : '100%',
              minHeight: previewMode === 'mobile' ? '852px' : '600px',
              backgroundColor: '#ffffff',
              border: '1px solid #d1d5db',
              borderRadius: '8px',
              padding: '20px',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
              position: 'relative',
              overflow: 'auto',
              ...(previewMode === 'mobile' ? {
                // Mobile safe area simulation using CSS variables
                '--safe-area-top': '47px',
                '--safe-area-bottom': '34px',
                '--safe-area-left': '0px',
                '--safe-area-right': '0px',
              } : {})
            }}
          >
            {schema.map(element => renderElement(element))}
            
            {/* Empty state when canvas is empty */}
            {schema.length === 0 && (
              <div style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100%',
                color: '#9ca3af',
                textAlign: 'center',
                padding: '20px'
              }}>
                <div style={{ fontSize: '48px', marginBottom: '16px' }}>📱</div>
                <h3 style={{ fontSize: '18px', fontWeight: '500', marginBottom: '8px' }}>Your canvas is empty</h3>
                <p>Drag elements from the toolbox to start building</p>
              </div>
            )}
          </div>
        </div>

        {/* Right properties panel */}
        <div 
          style={{
            width: '300px',
            backgroundColor: '#ffffff',
            borderLeft: '1px solid #e5e7eb',
            padding: '16px',
            display: 'flex',
            flexDirection: 'column',
            overflowY: 'auto'
          }}
          aria-label="Properties panel"
        >
          <h2 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px', color: '#374151' }}>
            Properties
          </h2>
          
          {selectedNode ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '6px', color: '#374151' }}>
                  Element Type
                </label>
                <input
                  type="text"
                  value={selectedNode.type}
                  readOnly
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    border: '1px solid #d1d5db',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                />
              </div>
              
              {/* Common properties */}
              <div>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '6px', color: '#374151' }}>
                  Padding
                </label>
                <input
                  type="text"
                  value={selectedNode.props.padding || ''}
                  onChange={(e) => handlePropChange('padding', e.target.value)}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    border: '1px solid #d1d5db',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                  aria-label="Padding property"
                />
              </div>
              
              <div>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '6px', color: '#374151' }}>
                  Text Align
                </label>
                <select
                  value={selectedNode.props.align || 'left'}
                  onChange={(e) => handlePropChange('align', e.target.value)}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    border: '1px solid #d1d5db',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                  aria-label="Text alignment property"
                >
                  <option value="left">Left</option>
                  <option value="center">Center</option>
                  <option value="right">Right</option>
                </select>
              </div>
              
              <div>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '6px', color: '#374151' }}>
                  Max Width
                </label>
                <input
                  type="text"
                  value={selectedNode.props.maxWidth || ''}
                  onChange={(e) => handlePropChange('maxWidth', e.target.value)}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    border: '1px solid #d1d5db',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                  aria-label="Max width property"
                />
              </div>
              
              {/* Type-specific properties */}
              {(selectedNode.type === 'heading' || selectedNode.type === 'text') && (
                <>
                  <div>
                    <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '6px', color: '#374151' }}>
                      Text Content
                    </label>
                    <textarea
                      value={selectedNode.props.text || ''}
                      onChange={(e) => handlePropChange('text', e.target.value)}
                      style={{
                        width: '100%',
                        padding: '8px 12px',
                        border: '1px solid #d1d5db',
                        borderRadius: '4px',
                        fontSize: '14px',
                        minHeight: '60px',
                        resize: 'vertical'
                      }}
                      aria-label="Text content property"
                    />
                  </div>
                  
                  <div>
                    <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '6px', color: '#374151' }}>
                      Font Size
                    </label>
                    <input
                      type="text"
                      value={selectedNode.props.fontSize || ''}
                      onChange={(e) => handlePropChange('fontSize', e.target.value)}
                      style={{
                        width: '100%',
                        padding: '8px 12px',
                        border: '1px solid #d1d5db',
                        borderRadius: '4px',
                        fontSize: '14px'
                      }}
                      aria-label="Font size property"
                    />
                  </div>
                </>
              )}
              
              {(selectedNode.type === 'section' || selectedNode.type === 'button') && (
                <div>
                  <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '6px', color: '#374151' }}>
                    Background Color
                  </label>
                  <input
                    type="color"
                    value={selectedNode.props.backgroundColor || '#ffffff'}
                    onChange={(e) => handlePropChange('backgroundColor', e.target.value)}
                    style={{
                      width: '100%',
                      padding: '4px',
                      border: '1px solid #d1d5db',
                      borderRadius: '4px',
                      fontSize: '14px',
                      height: '36px'
                    }}
                    aria-label="Background color property"
                  />
                </div>
              )}
              
              {selectedNode.type === 'button' && (
                <div>
                  <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '6px', color: '#374151' }}>
                    Text Color
                  </label>
                  <input
                    type="color"
                    value={selectedNode.props.color || '#ffffff'}
                    onChange={(e) => handlePropChange('color', e.target.value)}
                    style={{
                      width: '100%',
                      padding: '4px',
                      border: '1px solid #d1d5db',
                      borderRadius: '4px',
                      fontSize: '14px',
                      height: '36px'
                    }}
                    aria-label="Text color property"
                  />
                </div>
              )}
              
              {selectedNode.type === 'image' && (
                <>
                  <div>
                    <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '6px', color: '#374151' }}>
                      Image URL
                    </label>
                    <input
                      type="text"
                      value={selectedNode.props.src || ''}
                      onChange={(e) => handlePropChange('src', e.target.value)}
                      style={{
                        width: '100%',
                        padding: '8px 12px',
                        border: '1px solid #d1d5db',
                        borderRadius: '4px',
                        fontSize: '14px'
                      }}
                      aria-label="Image source URL"
                    />
                  </div>
                  
                  <div>
                    <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '6px', color: '#374151' }}>
                      Alt Text
                    </label>
                    <input
                      type="text"
                      value={selectedNode.props.alt || ''}
                      onChange={(e) => handlePropChange('alt', e.target.value)}
                      style={{
                        width: '100%',
                        padding: '8px 12px',
                        border: '1px solid #d1d5db',
                        borderRadius: '4px',
                        fontSize: '14px'
                      }}
                      aria-label="Image alt text"
                    />
                  </div>
                </>
              )}
              
              {/* Delete button */}
              <button
                onClick={handleDeleteNode}
                style={{
                  padding: '10px',
                  borderRadius: '6px',
                  backgroundColor: '#ef4444',
                  color: '#ffffff',
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '500',
                  marginTop: 'auto'
                }}
                aria-label="Delete selected element"
              >
                Delete Element
              </button>
            </div>
          ) : (
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              color: '#9ca3af',
              textAlign: 'center',
              padding: '20px'
            }}>
              <div style={{ fontSize: '24px', marginBottom: '12px' }}>⚙️</div>
              <h3 style={{ fontSize: '16px', fontWeight: '500', marginBottom: '8px' }}>No Selection</h3>
              <p style={{ fontSize: '14px' }}>Select an element to edit its properties</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default WebBuilderSimpleUI;