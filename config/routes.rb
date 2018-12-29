Rails.application.routes.draw do
  get 'pages/about'
  get 'pages/backtests'
  get 'pages/blog'
  get 'pages/compare'
  get 'pages/contact'
  get 'pages/whatif'
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  root 'pages#about'
end
