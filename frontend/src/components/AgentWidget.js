import { API_BASE_URL } from '../config';

export function AgentWidget() {
  return `
    <!-- Large Horizontal Dashboard Container -->
    <div class="relative w-full max-w-[1100px] h-[700px] rounded-2xl overflow-hidden shadow-2xl border border-brand-gold/10 flex bg-[#0a0a0a] mx-auto my-8 font-sans">
      
      <img src="/bg-aureeq-option3-seamless.png" class="absolute inset-0 w-full h-full object-cover opacity-70 z-0" alt="Background" />
      


      <!-- Luxury Gradient Overlays -->
      <div class="absolute inset-0 bg-gradient-to-r from-black/40 via-transparent to-black/20 pointer-events-none z-10"></div>
      <div class="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/60 pointer-events-none z-10"></div>
      
      <!-- 1. Left Side: Chat Interface (Full width for scrollbar) -->
      <div class="w-full flex flex-col relative z-30 pointer-events-none">
        <!-- Header (Back to pointer-events-auto for interactions) -->
        <div class="h-14 flex items-center justify-between px-6 bg-black/20 backdrop-blur-sm border-b border-white/5 pointer-events-auto relative">
          <img src="/aureeq-logo-text.png" class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 h-[88px] object-contain opacity-90" alt="Aureeq" />
          <div class="flex items-center gap-3">
            <span class="text-white font-medium text-sm tracking-wide">Aureeq Assistant</span>
          </div>
          <!-- Logout / Reset Identity Button -->
          <button id="logout-btn" class="text-white/50 hover:text-red-400 transition-colors z-50 pointer-events-auto" title="Reset Identity">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
          </button>
        </div>

        <!-- Chat Messages Area (Full width, pointer-events-auto) -->
        <style>
          #chat-messages::-webkit-scrollbar {
            width: 4px;
          }
          #chat-messages::-webkit-scrollbar-track {
            background: transparent;
          }
          #chat-messages::-webkit-scrollbar-thumb {
            background: rgba(212, 175, 55, 0.3);
            border-radius: 10px;
          }
          #chat-messages::-webkit-scrollbar-thumb:hover {
            background: rgba(212, 175, 55, 0.6);
          }
        </style>
        <div class="flex-1 overflow-y-auto p-8 pr-[30%] flex flex-col gap-6 scroll-smooth pointer-events-auto" id="chat-messages">
          <!-- AI Welcome Message -->
          <div class="animate-fade-in group max-w-[85%]">
             <div class="bg-brand-gold text-black text-[11px] font-bold px-4 py-1 rounded-t-xl w-full tracking-[0.2em] uppercase flex justify-between items-center">
               <span>Aureeq</span>
               <button id="welcome-play-btn" class="hidden hover:scale-110 transition-transform" title="Play Greeting">
                 <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
               </button>
             </div>
             <div id="welcome-message-text" class="bg-[#1a1a1a] border-x border-b border-white/5 text-slate-100 text-[15px] px-5 py-3 rounded-b-xl shadow-2xl leading-[1.5] font-normal font-inter msg-content">
               Hello I am AUREEQ your personal assistant, How may I help you today?
             </div>
          </div>
        </div>

        <!-- Footer: Input Area (Pointer-events-auto) -->
        <div class="h-24 px-8 pb-6 flex items-end gap-3 z-30 pointer-events-auto pr-[30%]">
          <button id="mic-btn" class="flex w-12 h-12 rounded-xl bg-brand-black/40 border border-brand-gold/20 items-center justify-center text-brand-gold hover:bg-brand-gold hover:text-black transition-all group shrink-0 backdrop-blur-md">
            <svg id="mic-icon" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path d="M17 11c0 3.01-2.55 5.5-5.5 5.5S6 14.01 6 11H4c0 3.53 2.61 6.43 6 6.92V21h4v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>
          </button>

          <div class="flex-1 relative">
            <input id="chat-input" type="text" placeholder="Write message here..." autocomplete="off"
              class="w-full bg-brand-black/60 border border-white/10 rounded-xl h-12 px-5 text-white text-sm placeholder-gray-500 focus:outline-none focus:border-brand-gold/40 transition-colors shadow-2xl backdrop-blur-md" />
          </div>

          <button id="send-btn" class="w-12 h-12 rounded-xl bg-brand-gold/80 flex items-center justify-center shadow-lg shadow-brand-gold/20 hover:bg-brand-gold transition-all group shrink-0 backdrop-blur-md">
            <svg class="w-5 h-5 text-black group-hover:translate-x-0.5 transition-transform" fill="currentColor" viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
          </button>
        </div>
      </div>

      <!-- 2. Right Side: Avatar (30% absolute) -->
      <div class="absolute top-0 right-0 bottom-0 w-[30%] overflow-hidden flex flex-col z-20 pointer-events-none">
        <!-- 3D Canvas Container -->
        <div class="absolute inset-0 flex items-end justify-center pointer-events-none translate-y-12">
          <canvas id="avatar-canvas" class="w-full h-full object-contain pointer-events-none"></canvas>
        </div>
      </div>

    <!-- 3. Microphone Permission Modal -->
    <div id="mic-permission-modal" class="absolute inset-0 z-[101] bg-black/80 backdrop-blur-md flex items-center justify-center hidden">
        <div class="max-w-[400px] w-full bg-[#111] border border-brand-gold/20 rounded-2xl p-8 shadow-[0_0_50px_rgba(212,175,55,0.15)] animate-fade-in text-center">
            <div class="w-20 h-20 bg-brand-gold/10 rounded-full flex items-center justify-center text-4xl mb-6 mx-auto">
                🎙️
            </div>
            <h3 class="text-white text-xl font-bold mb-2">Microphone Access</h3>
            <p class="text-white/60 text-sm mb-8">Aureeq needs microphone access for voice interactions. Would you like to enable it?</p>
            
            <div class="flex gap-4">
                <button id="mic-deny-btn" class="flex-1 h-12 bg-white/5 text-white/70 font-bold text-sm rounded-xl hover:bg-white/10 transition-all uppercase tracking-widest">
                    Maybe Later
                </button>
                <button id="mic-grant-btn" class="flex-1 h-12 bg-brand-gold text-black font-bold text-sm rounded-xl shadow-lg shadow-brand-gold/20 hover:scale-[1.02] active:scale-[0.98] transition-all uppercase tracking-widest">
                    Grant Access
                </button>
            </div>
        </div>
    </div>

    <!-- 4. Mandatory Onboarding Modal -->
      <div id="onboarding-modal" class="absolute inset-0 z-[100] bg-black/80 backdrop-blur-md flex items-center justify-center hidden">
        <div class="max-w-[400px] w-full bg-[#111] border border-brand-gold/20 rounded-2xl p-8 shadow-[0_0_50px_rgba(212,175,55,0.15)] animate-fade-in">
          <div class="text-center mb-6">
            <div class="text-brand-gold text-4xl font-black mb-2 tracking-tighter">AUREEQ</div>
            <p class="text-white/60 text-xs tracking-[0.2em] font-bold uppercase">Sales Strategist Onboarding</p>
          </div>
          
          <div class="space-y-4">
            <div>
              <label class="block text-brand-gold/60 text-[10px] font-bold uppercase tracking-widest mb-1 ml-1 text-left">Full Name</label>
              <input id="ob-name" type="text" placeholder="Enter your name" class="w-full bg-white/5 border border-white/10 rounded-xl h-12 px-5 text-white text-sm focus:outline-none focus:border-brand-gold/40 transition-all shadow-inner" />
            </div>
            <div>
              <label class="block text-brand-gold/60 text-[10px] font-bold uppercase tracking-widest mb-1 ml-1 text-left">Email Address</label>
              <input id="ob-email" type="email" placeholder="email@example.com" class="w-full bg-white/5 border border-white/10 rounded-xl h-12 px-5 text-white text-sm focus:outline-none focus:border-brand-gold/40 transition-all shadow-inner" />
            </div>
            
            <button id="ob-submit" class="w-full h-12 bg-brand-gold text-black font-black text-sm rounded-xl shadow-lg shadow-brand-gold/20 hover:scale-[1.02] active:scale-[0.98] transition-all uppercase tracking-widest mt-4">
              Access Strategist
            </button>
          </div>
          
          <p class="text-white/30 text-[9px] text-center mt-6 uppercase tracking-tight">Your data is synced securely to the Aureeq persistence layer.</p>
        </div>
      </div>

    </div>
  `;
}

export function setupAgentInteraction(avatarRenderer) {
  // Session is now persisted across reloads
  // localStorage.removeItem('aureeq_user_name');
  // localStorage.removeItem('aureeq_user_email');

  const input = document.getElementById('chat-input');
  const sendBtn = document.getElementById('send-btn');
  const messagesContainer = document.getElementById('chat-messages');

  // Logic for Logout Button
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      if (confirm("Reset identity and show onboarding again?")) {
        localStorage.removeItem('aureeq_user_name');
        localStorage.removeItem('aureeq_user_email');
        localStorage.removeItem('aureeq_user_prefs');
        location.reload(); // Reload to trigger onboarding check
      }
    });
  }

  // --- LUXURY ORDER POPUP UI ---
  const modalHtml = `
    <div id="order-modal" class="hidden absolute inset-0 z-[200] bg-black/80 backdrop-blur-md flex items-center justify-center p-6 animate-fade-in pointer-events-auto">
        <div class="bg-[#121212] border border-brand-gold/20 rounded-[2rem] p-8 w-full max-w-sm shadow-[0_0_50px_rgba(212,175,55,0.15)] transform scale-100 transition-all flex flex-col items-center">
            
            <!-- Food Icon Container -->
            <div class="w-20 h-20 bg-brand-gold/10 rounded-full flex items-center justify-center mb-6 shadow-inner border border-brand-gold/10">
                <img src="https://img.icons8.com/ios-filled/50/d4af37/restaurant.png" class="w-10 h-10 object-contain" id="modal-icon-img" alt="Order" />
            </div>
            
            <h3 class="text-white text-2xl font-black mb-1 tracking-tight" id="modal-title">Confirm Order</h3>
            <p class="text-white/50 text-xs uppercase tracking-widest mb-8" id="modal-subtitle">Would you like to add this to your cart?</p>

            <!-- Item Display Row -->
            <div class="bg-[#1a1a1a] border border-white/5 rounded-2xl p-5 w-full flex justify-between items-center mb-10 shadow-inner">
                <span id="modal-item-name" class="text-white font-bold text-lg tracking-tight">Item Name</span>
                <span id="modal-item-price" class="text-brand-gold font-black text-lg">£0.00</span>
            </div>

            <!-- Action Buttons -->
            <div class="flex gap-4 w-full">
                <button id="modal-cancel-btn" class="flex-1 h-14 bg-white/5 hover:bg-white/10 text-white/70 font-bold text-sm rounded-2xl transition-all uppercase tracking-widest border border-white/5">
                    Cancel
                </button>
                <button id="modal-confirm-btn" class="flex-1 h-14 bg-brand-gold hover:bg-[#c4a034] text-black font-black text-sm rounded-2xl shadow-lg shadow-brand-gold/20 transition-all uppercase tracking-widest active:scale-95">
                    Add to Cart
                </button>
            </div>
        </div>
    </div>`;

  // Inject if not present
  const widgetContainer = document.querySelector('.relative.w-full.max-w-\\[1100px\\]');
  if (widgetContainer && !document.getElementById('order-modal')) {
    const temp = document.createElement('div');
    temp.innerHTML = modalHtml;
    widgetContainer.appendChild(temp.firstElementChild);
  }

  const orderModal = document.getElementById('order-modal');
  const modalName = document.getElementById('modal-item-name');
  const modalPrice = document.getElementById('modal-item-price');
  const modalConfirm = document.getElementById('modal-confirm-btn');
  const modalCancel = document.getElementById('modal-cancel-btn');

  const showOrderPopup = (name, price, isRemove = false, wp_id = '') => {
    if (!orderModal) return;

    // Clean price string for display if needed
    let displayPrice = price;
    if (!displayPrice.toString().startsWith('£')) displayPrice = `£${displayPrice}`;

    modalName.textContent = name;
    modalPrice.textContent = displayPrice;

    const modalTitle = document.getElementById('modal-title');
    const modalSubtitle = document.getElementById('modal-subtitle');
    const modalConfirmBtn = document.getElementById('modal-confirm-btn');
    const modalIconImg = document.getElementById('modal-icon-img');

    if (isRemove) {
      modalTitle.textContent = "Remove Item";
      modalSubtitle.textContent = "Remove this from your cart?";
      modalConfirmBtn.textContent = "Remove";
      modalConfirmBtn.className = "flex-1 h-14 bg-red-900/40 hover:bg-red-800 text-red-200 font-bold text-sm rounded-2xl transition-all uppercase tracking-widest border border-red-500/20";
      if (modalIconImg) modalIconImg.src = "https://img.icons8.com/ios-filled/50/ff4444/trash.png";
    } else {
      modalTitle.textContent = "Confirm Order";
      modalSubtitle.textContent = "Would you like to add this to your cart?";
      modalConfirmBtn.textContent = "Add to Cart";
      modalConfirmBtn.className = "flex-1 h-14 bg-brand-gold hover:bg-[#c4a034] text-black font-black text-sm rounded-2xl shadow-lg shadow-brand-gold/20 transition-all uppercase tracking-widest active:scale-95";
      if (modalIconImg) modalIconImg.src = "https://img.icons8.com/ios-filled/50/d4af37/restaurant.png";
    }

    orderModal.classList.remove('hidden');

    modalConfirmBtn.onclick = () => {
      const type = isRemove ? 'remove_from_cart' : 'add_to_cart';

      // FUNCTIONAL INTEGRATION: Broadcase to WordPress Host
      window.parent.postMessage({
        type: type,
        action: 'woocommerce_cart_action',
        product: {
          name: name,
          price: price,
          id: wp_id,
          sku: wp_id
        },
        source: 'aureeq_ai'
      }, '*');

      const user = getStoredUser();
      if (!isRemove) {
        fetch(`${API_BASE_URL}/order`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_id: user.email,
            items: [name],
            total: parseFloat(price.toString().replace(/[^0-9.]/g, '')),
            wp_id: wp_id
          })
        });
      }

      addMessage(isRemove ? `❌ **${name}** removed from cart.` : `✅ **${name}** added to your cart!`, false);
      orderModal.classList.add('hidden');
    };

    modalCancel.onclick = () => {
      orderModal.classList.add('hidden');
    };
  };

  if (!input || !sendBtn) return;

  const addMessage = (text, isUser = false) => {
    const div = document.createElement('div');
    div.className = "animate-fade-in mb-4";

    if (isUser) {
      div.innerHTML = `
                <div class="flex justify-end">
                    <div class="max-w-[85%]">
                        <div class="bg-[#1a1a1a] text-white text-[11px] font-bold px-4 py-1 rounded-t-xl w-full tracking-[0.2em] uppercase">User</div>
                        <div class="bg-brand-gold text-black text-[15px] px-5 py-3 rounded-b-xl shadow-2xl leading-[1.5] font-normal font-inter">${text}</div>
                    </div>
                </div>`;
    } else {
      let displayText = text;
      const orderMatch = text.match(/\[ORDER:\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)?\]/i);
      const removeMatch = text.match(/\[REMOVE:\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)?\]/i);

      if (orderMatch) {
        const name = orderMatch[1].trim();
        const price = orderMatch[2].trim();
        const wp_id = (orderMatch[3] || "").trim();
        displayText = text.replace(orderMatch[0], '').trim();
        setTimeout(() => showOrderPopup(name, price, false, wp_id), 800);
      } else if (removeMatch) {
        const name = removeMatch[1].trim();
        const price = removeMatch[2].trim();
        const wp_id = (removeMatch[3] || "").trim();
        displayText = text.replace(removeMatch[0], '').trim();
        setTimeout(() => showOrderPopup(name, price, true, wp_id), 800);
      }

      // Support Markdown links and newlines in static messages + Tag stripping
      displayText = displayText
        .replace(/\[ORDER:\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)?\]/gi, '')
        .replace(/\[REMOVE:\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)?\]/gi, '')
        .replace(/\n/g, "<br/>")
        .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" class="text-brand-gold underline hover:text-yellow-400 break-all">$1</a>');

      div.innerHTML = `
                <div class="max-w-[85%]">
                  <div class="bg-brand-gold text-black text-[11px] font-bold px-4 py-1 rounded-t-xl w-full tracking-[0.2em] uppercase">Aureeq</div>
                  <div class="bg-[#1a1a1a] border-x border-b border-white/5 text-slate-100 text-[15px] px-5 py-3 rounded-b-xl shadow-2xl leading-[1.5] font-normal font-inter msg-content">${displayText}</div>
                </div>`;
    }
    messagesContainer.appendChild(div);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return div;
  };

  const resolveAudioUrl = (path) => {
    if (!path) return null;
    if (path.startsWith('http') || path.startsWith('data:')) return path;

    // Clean up base and path
    const cleanBase = API_BASE_URL.replace(/\/$/, '');
    const cleanPath = path.startsWith('/') ? path : `/${path}`;

    // If path already includes API_BASE_URL, don't duplicate
    const finalPath = cleanPath.startsWith(cleanBase) ? cleanPath : `${cleanBase}${cleanPath}`;

    try {
      return new URL(finalPath, window.location.origin).href;
    } catch (e) {
      console.error("URL Resolution Error:", e);
      return `${window.location.origin}${finalPath}`;
    }
  };

  const getStoredUser = () => ({
    name: localStorage.getItem('aureeq_user_name') || 'Guest',
    email: localStorage.getItem('aureeq_user_email') || null,
    preferences: localStorage.getItem('aureeq_user_prefs') || ''
  });

  let isVoiceInputSource = false;

  const handleSend = async () => {
    const text = input.value.trim();
    if (!text) return;

    const wasVoice = isVoiceInputSource;
    isVoiceInputSource = false;

    // Detect Identity in text if needed
    // (omitted simple identify logic for brevity, main focus is send)

    addMessage(text, true);
    input.value = '';

    const user = getStoredUser();

    import('../lib/salesAgent').then(async ({ SalesAgent }) => {
      // Assemble context using RAG/etc on client side helper if needed, 
      // but here we just pass text to backend which handles heavy lifting
      const context = await SalesAgent.assembleContext(text, user);

      let aiMsgDiv = addMessage("Aureeq is thinking...");
      let contentEl = aiMsgDiv.querySelector('.msg-content');

      const res = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, user_id: user.email, context: context, user_metadata: user, was_voice: wasVoice })
      });

      if (!res.ok) {
        const errorText = await res.text();
        contentEl.innerText = `Error: Backend returned ${res.status}. ${errorText}`;
        console.error("Chat Request Failed:", res.status, errorText);
        return;
      }

      let fullText = "";
      try {
        const reader = res.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let hasTokens = false;

        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            console.log("Stream complete. Full text length:", fullText.length);
            break;
          }

          const chunk = decoder.decode(value, { stream: true });
          console.log("RX Chunk:", chunk);

          if (!hasTokens) {
            // Check if chunk has visible content (ignore ZWSP \u200B and whitespace)
            const isVisible = chunk.replace(/[\u200B\s]/g, '').length > 0;
            if (!isVisible) continue;

            contentEl.textContent = "";
            hasTokens = true;
          }

          fullText += chunk;

          // --- START AUDIO TAG PARSING ---
          if (fullText.includes("|AUDIO_URL|")) {
            const parts = fullText.split("|AUDIO_URL|");
            const messagePart = parts[0];
            const audioParts = parts[1].split("|TEXT|");

            if (audioParts.length > 1) {
              const audioUrlPath = audioParts[0];
              const finalMessage = audioParts[1];

              // Update UI with clean message (Audio Case)
              const cleanText = finalMessage
                .replace(/\[ORDER:\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)?\]/gi, '')
                .replace(/\[REMOVE:\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)?\]/gi, '')
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/\n/g, "<br/>")
                .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" class="text-brand-gold underline hover:text-yellow-400 break-all">$1</a>');

              contentEl.innerHTML = cleanText;

              // Play Audio
              const fullAudioUrl = resolveAudioUrl(audioUrlPath);
              console.log("Playing streamed audio:", fullAudioUrl);

              fetch(fullAudioUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: finalMessage })
              })
                .then(r => r.arrayBuffer())
                .then(async buffer => {
                  if (window.avatarFunctions && window.avatarFunctions.speak) {
                    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    const audioBuffer = await audioCtx.decodeAudioData(buffer);
                    window.avatarFunctions.speak(audioBuffer);
                  } else {
                    const blob = new Blob([buffer], { type: 'audio/wav' });
                    const url = URL.createObjectURL(blob);
                    new Audio(url).play().catch(e => console.error("Audio playback error:", e));
                  }
                })
                .catch(e => console.error("TTS Fetch Error:", e));

              // Check for tags in the final message of an audio response
              const orderMatch = finalMessage.match(/\[ORDER:\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)?\]/i);
              const removeMatch = finalMessage.match(/\[REMOVE:\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)?\]/i);
              if (orderMatch) {
                const name = orderMatch[1].trim();
                const price = orderMatch[2].trim();
                const wp_id = (orderMatch[3] || "").trim();
                setTimeout(() => showOrderPopup(name, price, false, wp_id), 800);
              } else if (removeMatch) {
                const name = removeMatch[1].trim();
                const price = removeMatch[2].trim();
                const wp_id = (removeMatch[3] || "").trim();
                setTimeout(() => showOrderPopup(name, price, true, wp_id), 800);
              }

              break;
            }
          }
          // --- END AUDIO TAG PARSING ---

          // Simple Markdown Link Converter + Tag Stripper
          const safeText = fullText
            .replace(/\[ORDER:\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)?\]/gi, '')
            .replace(/\[REMOVE:\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)?\]/gi, '')
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/\n/g, "<br/>")
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" class="text-brand-gold underline hover:text-yellow-400 break-all">$1</a>');

          contentEl.innerHTML = safeText;
          messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        if (!hasTokens || !fullText.trim()) {
          contentEl.textContent = "The brain is cooling down. Please try again.";
        }
      } catch (streamError) {
        console.error("Stream interrupted:", streamError);
        contentEl.innerText += "\n[Connection interrupted. Please try again.]";
      }

      // Check order tag again in full text for safety (if not already handled by audio block)
      const orderMatchFull = fullText.match(/\[ORDER:\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)?\]/i);
      const removeMatchFull = fullText.match(/\[REMOVE:\s*(.*?)\s*\|\s*(.*?)?\]/i);

      if (orderMatchFull && !fullText.includes("|AUDIO_URL|")) {
        const name = orderMatchFull[1].trim();
        const price = orderMatchFull[2].trim();
        const wp_id = (orderMatchFull[3] || "").trim();
        setTimeout(() => showOrderPopup(name, price, false, wp_id), 500);
      } else if (removeMatchFull && !fullText.includes("|AUDIO_URL|")) {
        const name = removeMatchFull[1].trim();
        const price = removeMatchFull[2].trim();
        const wp_id = (removeMatchFull[3] || "").trim();
        setTimeout(() => showOrderPopup(name, price, true, wp_id), 500);
      }

    });
  };

  sendBtn.onclick = handleSend;
  input.onkeypress = (e) => { if (e.key === 'Enter') handleSend(); };

  // --- STRICT MIC LOGIC ---
  const micBtn = document.getElementById('mic-btn');
  const micIcon = document.getElementById('mic-icon');
  let recognition = null;
  let isRecording = false;

  const initRecognition = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return null;
    const rec = new SpeechRecognition();
    rec.continuous = true;
    rec.interimResults = true;
    rec.lang = 'en-US';

    rec.onresult = (e) => {
      let fullTranscript = '';
      for (let i = 0; i < e.results.length; ++i) {
        fullTranscript += e.results[i][0].transcript;
      }
      input.value = fullTranscript;
      isVoiceInputSource = true;
    };

    rec.onend = () => {
      if (isRecording) {
        isRecording = false;
        micBtn.classList.remove('bg-red-500', 'animate-pulse');
        micIcon.innerHTML = '<path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path d="M17 11c0 3.01-2.55 5.5-5.5 5.5S6 14.01 6 11H4c0 3.53 2.61 6.43 6 6.92V21h4v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>';
      }
    };

    return rec;
  };

  micBtn.onclick = async () => {
    // 1. Check for stored permission preference
    const hasPermission = localStorage.getItem('aureeq_mic_permission') === 'granted';

    if (!hasPermission) {
      const permModal = document.getElementById('mic-permission-modal');
      const grantBtn = document.getElementById('mic-grant-btn');
      const denyBtn = document.getElementById('mic-deny-btn');

      if (permModal) {
        permModal.classList.remove('hidden');

        grantBtn.onclick = async () => {
          try {
            await navigator.mediaDevices.getUserMedia({ audio: true });
            localStorage.setItem('aureeq_mic_permission', 'granted');
            permModal.classList.add('hidden');
            // Recurse to start recording
            micBtn.click();
          } catch (e) {
            console.error("Mic Permission Denied:", e);
            alert("Microphone permission is required for voice input.");
            permModal.classList.add('hidden');
          }
        };

        denyBtn.onclick = () => {
          permModal.classList.add('hidden');
        };
      }
      return;
    }

    // 2. If currently recording -> STOP and SEND
    if (isRecording) {
      if (recognition) {
        recognition.stop();
        isRecording = false;
        micBtn.classList.remove('bg-red-500', 'animate-pulse');
        micIcon.innerHTML = '<path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path d="M17 11c0 3.01-2.55 5.5-5.5 5.5S6 14.01 6 11H4c0 3.53 2.61 6.43 6 6.92V21h4v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>';

        // Auto-send after a small delay to catch the last word
        setTimeout(() => {
          if (input.value.trim().length > 0) handleSend();
        }, 300);
      }
    } else {
      // 3. If NOT recording -> START
      try {
        if (!recognition) recognition = initRecognition();
        if (recognition) {
          input.value = ''; // Clear previous text for a fresh start
          recognition.start();
          isVoiceInputSource = true;
          isRecording = true;
          micBtn.classList.add('bg-red-500', 'animate-pulse');
          // Change icon to Square (Stop)
          micIcon.innerHTML = '<rect x="6" y="6" width="12" height="12" />';
        } else {
          alert("Speech Recognition not supported in this browser.");
        }
      } catch (e) {
        console.error("Mic Start Error:", e);
      }
    }
  };

  // Onboarding Logic (Simplified for check)
  const modal = document.getElementById('onboarding-modal');
  const checkOnboarding = () => {
    const user = getStoredUser();
    if (!user.email || !user.name) {
      if (modal) modal.classList.remove('hidden');
      return false;
    }
    if (modal) modal.classList.add('hidden');
    return true;
  };

  const obSubmit = document.getElementById('ob-submit');
  if (obSubmit) {
    obSubmit.onclick = () => {
      const name = document.getElementById('ob-name').value;
      const email = document.getElementById('ob-email').value;
      if (name && email) {
        localStorage.setItem('aureeq_user_name', name);
        localStorage.setItem('aureeq_user_email', email);
        checkOnboarding();
        initWelcome(name);
      }
    };
  }

  const isOnboarded = checkOnboarding();
  const initWelcome = async (name) => {
    try {
      const user = getStoredUser();
      const userName = name || user.name || "Guest";

      console.log("Initializing welcome for:", userName);

      const res = await fetch(`${API_BASE_URL}/welcome?name=${encodeURIComponent(userName)}&user_id=${encodeURIComponent(user.email || "")}`);
      const data = await res.json();

      if (data.response) {
        const welcomeTextEl = document.getElementById('welcome-message-text');
        if (welcomeTextEl) welcomeTextEl.textContent = data.response;
      }

      if (data.audio_url) {
        const fullWelcomeUrl = resolveAudioUrl(data.audio_url);
        const playBtn = document.getElementById('welcome-play-btn');

        const playAudio = async () => {
          try {
            if (window.avatarFunctions && window.avatarFunctions.speakFromUrl) {
              await window.avatarFunctions.speakFromUrl(fullWelcomeUrl);
            } else {
              const audio = new Audio(fullWelcomeUrl);
              await audio.play();
            }
            if (playBtn) playBtn.classList.add('hidden');
          } catch (e) {
            console.warn("Auto-play blocked, showing play button:", e);
            if (playBtn) {
              playBtn.classList.remove('hidden');
              playBtn.onclick = () => playAudio();
            }
          }
        };

        playAudio();
      }
    } catch (e) {
      console.error("Welcome init failed:", e);
    }
  };

  if (isOnboarded) {
    // Small delay to ensure everything is loaded
    setTimeout(() => initWelcome(), 1000);
  }
}
