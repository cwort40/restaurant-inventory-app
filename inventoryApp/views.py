

from chartjs.views.lines import BaseLineChartView
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, TemplateView

from inventoryApp.constants.util import UnitConversionUtil
from inventoryApp.forms import IngredientForm, MenuItemForm, RecipeRequirementForm, CustomUserCreationForm
from inventoryApp.models import Ingredient, MenuItem, Purchase, RecipeRequirement


# Define 2 functions to render HTML pages
def base(request):
    # Render the base.html page
    return render(request, 'inventoryApp/base.html')


# Login view that redirects user to about page
class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html'
    success_url = '/'


# Register view that redirects user to about page
class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('about')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


# handles logout request and redirects user to login page
def log_out(request):
    logout(request)
    return redirect("/accounts/login")


# About page
class AboutView(TemplateView):
    template_name = 'inventoryApp/about.html'


# Define ListView to display a list of ingredients
class IngredientListView(LoginRequiredMixin, ListView):
    # Displays a list of ingredients
    template_name = 'inventoryApp/ingredients.html'
    model = Ingredient
    ordering = ['name']
    paginate_by = 15

    def get_queryset(self):
        # Filter the queryset based on a search term
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        search_term = self.request.GET.get('search', None)
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)
        # Check if queryset is empty
        if not queryset.exists():
            messages.info(self.request, 'No results found.')
        return queryset


# Define UpdateView, CreateView, and DeleteView for ingredients
class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    # Update an ingredient
    template_name = 'inventoryApp/update-ingredient.html'
    model = Ingredient
    form_class = IngredientForm
    success_url = '/ingredients'

    # Form validation for current user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class IngredientCreateView(LoginRequiredMixin, CreateView):
    # Create an ingredient
    template_name = "inventoryApp/add-ingredient.html"
    model = Ingredient
    form_class = IngredientForm
    success_url = '/ingredients'

    # Form validation for current user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    # Delete an ingredient
    template_name = "inventoryApp/delete-ingredient.html"
    model = Ingredient
    success_url = '/ingredients'


# Define ListView to display a list of purchases
class PurchaseListView(LoginRequiredMixin, ListView):
    # Displays a list of purchases
    template_name = 'inventoryApp/purchases.html'
    model = Purchase
    ordering = ['timestamp']
    paginate_by = 15

    def get_queryset(self):
        # Filter the queryset based on a search term
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        search_term = self.request.GET.get('search', None)
        if search_term:
            queryset = queryset.filter(menu_item__title__icontains=search_term)
        return queryset


# Define PurchaseAddView to add a purchase
class PurchaseAddView(LoginRequiredMixin, TemplateView):
    # Add a purchase
    template_name = "inventoryApp/add-purchase.html"

    # Checks if menu item is available
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_items"] = [X for X in MenuItem.objects.all().filter(user=self.request.user) if X.available()]
        return context

    # Removes the ingredients from the inventory that were used to make the menu item
    def post(self, request):
        menu_item_id = request.POST["menu_item"]
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirement_set.all().filter(user=self.request.user)
        purchase = Purchase(menu_item=menu_item, user=self.request.user)

        for requirement in requirements:
            required_ingredient = requirement.ingredient
            required_quantity = requirement.quantity
            required_unit = requirement.unit
            available_quantity = required_ingredient.quantity
            available_unit = required_ingredient.unit
            if required_unit != available_unit:
                # convert the required quantity to a common unit
                required_quantity = UnitConversionUtil.convert_to_common_unit(required_quantity, required_unit,
                                                                              required_ingredient.name)
                available_quantity = UnitConversionUtil.convert_to_common_unit(available_quantity, available_unit,
                                                                               required_ingredient.name)

            if required_quantity <= available_quantity:
                # subtract the required quantity from the available quantity
                available_quantity -= required_quantity
                # convert the available quantity back to the original unit
                if required_unit != available_unit:
                    available_quantity = UnitConversionUtil.convert_to_original_unit(available_quantity, available_unit,
                                                                                     required_ingredient.name)

                required_ingredient.quantity = available_quantity
                required_ingredient.save()
            else:
                # handle insufficient inventory error
                return HttpResponse(f"Not enough {required_ingredient.name} in inventory")

        # save the purchase object
        purchase.save()

        # redirect to a success page
        return redirect("/purchases")


# Define purchase delete view
class PurchaseDeleteView(LoginRequiredMixin, DeleteView):
    # Delete a purchase
    template_name = "inventoryApp/delete-purchase.html"
    model = Purchase
    success_url = '/purchases'


# Define ListView to display a list of menu items
class MenuListView(LoginRequiredMixin, ListView):
    # Displays a list of menu items
    template_name = 'inventoryApp/menu.html'
    model = MenuItem
    ordering = ['title']
    paginate_by = 5

    def get_queryset(self):
        # Filter the queryset based on a search term
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('reciperequirement_set__ingredient')
        queryset = queryset.filter(user=self.request.user)
        search_term = self.request.GET.get('search', None)
        if search_term:
            queryset = queryset.filter(title__icontains=search_term)
        return queryset


# Define UpdateView, CreateView, and DeleteView for menu items
class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    # Update a menu item
    template_name = 'inventoryApp/update-menu-item.html'
    model = MenuItem
    form_class = MenuItemForm
    success_url = '/menu'

    # Form validation for current user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MenuItemCreateView(LoginRequiredMixin, CreateView):
    # Create a menu item
    template_name = "inventoryApp/add-menu-item.html"
    model = MenuItem
    form_class = MenuItemForm
    success_url = '/menu'

    # Form validation for current user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Add a new recipe requirement
class NewRecipeRequirementView(LoginRequiredMixin, CreateView):
    # Create a recipe requirement
    template_name = "inventoryApp/add-recipe-requirement.html"
    model = RecipeRequirement
    form_class = RecipeRequirementForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # Form validation for current user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    # Delete a menu item
    template_name = "inventoryApp/delete-menu-item.html"
    model = MenuItem
    success_url = '/menu'


# Define RestaurantSummaryView to display restaurant metrics
class RestaurantSummaryView(LoginRequiredMixin, View):
    # Displays a restaurant summary
    def get(self, request, *args, **kwargs):
        ingredients = Ingredient.objects.all().filter(user=request.user)
        purchases = Purchase.objects.all().filter(menu_item__user=request.user)

        # Calculate the total cost of inventory, total revenue, and total profit
        total_cost_of_inventory, total_revenue, total_profit = 0, 0, 0
        if ingredients and purchases:
            total_cost_of_inventory = sum(
                [ingredient.quantity * ingredient.price_per_unit for ingredient in ingredients])
            total_revenue = sum([purchase.menu_item.price for purchase in purchases])
            total_profit = total_revenue - total_cost_of_inventory

        context = {
            "total_cost_of_inventory": total_cost_of_inventory,
            "total_revenue": total_revenue,
            "total_profit": total_profit,
        }

        return render(request, "inventoryApp/insights.html", context)


# Define IngredientChartView to display a bar chart of ingredients
class IngredientChartView(LoginRequiredMixin, BaseLineChartView):
    def get_labels(self):
        # Return the names of the ingredients as labels
        return ['']

    def get_providers(self):
        # Return names of datasets with unit
        return ["{} ({})".format(ingredient.name, ingredient.unit) for ingredient in
                Ingredient.objects.all().filter(user=self.request.user)]

    def get_data(self):
        # Return the quantities of the ingredients as data
        return ["{:.1f}".format(ingredient.quantity) for ingredient in Ingredient.objects.all().filter(user=self.request.user)]


# Define view to render reports template
ingredient_chart = TemplateView.as_view(template_name='inventoryApp/insights.html')

# Define view to render JSON data for line chart
ingredient_chart_json = IngredientChartView.as_view()


# Define PurchaseLineChartView to display a bar chart of purchases
class PurchaseChartView(LoginRequiredMixin, BaseLineChartView):
    def get_labels(self):
        # Return the days of the week labels.
        return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def get_providers(self):
        # Return names of menu items.
        return [item.title for item in MenuItem.objects.all().filter(user=self.request.user)]

    def get_data(self):
        # Return the quantities purchased of each menu item as data.
        data = []
        today = timezone.now().date()
        one_week_ago = today - timezone.timedelta(days=7)

        for item in MenuItem.objects.all():
            item_purchases = Purchase.objects.filter(menu_item=item, timestamp__gte=one_week_ago, user=self.request.user)
            day_counts = [0, 0, 0, 0, 0, 0, 0]
            for purchase in item_purchases:
                day_counts[(purchase.timestamp.weekday()) % 7] += 1
            data.append(day_counts)
        return data


# Define view to render reports template
purchase_chart = TemplateView.as_view(template_name='inventoryApp/insights.html')

# Define view to render JSON data for line chart
purchase_chart_json = PurchaseChartView.as_view()
